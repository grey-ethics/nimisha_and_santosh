/**
 * generateApi.mjs
 * -------------
 * Reads an OpenAPI JSON file and creates axios wrapper files under src/services/generated/.
 *
 * How it finds openapi.json (first that exists):
 *  - ../nimisha_and_santosh/openapi.json
 *  - ../backend/openapi.json
 *  - ../openapi.json
 *
 * Usage:
 *   npm run gen:api
 *
 * Notes:
 * - This is a minimal generator tailored to your spec (paths, tags).
 * - It groups endpoints by the first tag if present, otherwise by path segment.
 * - Extend as your API grows (types, parameters, etc).
 */
import fs from "fs";
import path from "path";
import url from "url";

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, "..");
const candidates = [
  path.resolve(projectRoot, "../nimisha_and_santosh/openapi.json"),
  path.resolve(projectRoot, "../backend/openapi.json"),
  path.resolve(projectRoot, "../openapi.json")
];
const outDir = path.resolve(projectRoot, "src/services/generated");

const openapiPath = candidates.find(p => fs.existsSync(p));
if (!openapiPath) {
  console.log("No openapi.json found next to frontend. Skipping.");
  process.exit(0);
}

const spec = JSON.parse(fs.readFileSync(openapiPath, "utf-8"));
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

/** util: safe ts name */
const safe = (s) => s.replace(/[^a-zA-Z0-9_]/g, "_");

/** very small return type guesser */
const guessReturn = (op) => {
  const r200 = op?.responses?.["200"]?.content?.["application/json"]?.schema;
  if (!r200) return "any";
  if (r200.$ref) return "any";
  if (r200.type === "array") return "any[]";
  return "any";
};

const groups = {};
for (const [p, pathItem] of Object.entries(spec.paths || {})) {
  for (const method of Object.keys(pathItem)) {
    const op = pathItem[method];
    if (!op || typeof op !== "object") continue;
    const tag = (op.tags && op.tags[0]) || p.split("/")[1] || "misc";
    const group = safe(tag).toLowerCase();
    groups[group] ??= [];
    groups[group].push({ path: p, method: method.toUpperCase(), op });
  }
}

const header = (title) => `/**
 * Generated client for ${title}
 * (Minimal axios wrappers)
 */
import type { AxiosInstance } from "axios";
`;

for (const [group, items] of Object.entries(groups)) {
  const lines = [header(group)];
  for (const item of items) {
    const nameBase =
      item.op.operationId
        ? safe(item.op.operationId)
        : safe(`${item.method}_${item.path.replace(/[{}]/g, "")}`);
    const fname = nameBase.replace(/_{2,}/g, "_");
    const ret = guessReturn(item.op);
    const hasBody = !!item.op.requestBody?.content?.["application/json"]?.schema;
    const hasParamsInPath = item.path.includes("{");

    const pathParams = [];
    const pathFinal = item.path.replace(/{([^}]+)}/g, (_, p1) => {
      pathParams.push(p1);
      return "${" + p1 + "}";
    });

    const paramsSig = [];
    if (hasParamsInPath) paramsSig.push(...pathParams.map((p) => `${p}: string`));
    if (item.method === "GET") {
      // query params if any 'parameters' with in: 'query'
      const q = (item.op.parameters || []).filter((p) => p.in === "query");
      if (q.length) paramsSig.push(`params: { ${q.map((x) => `${x.name}: string`).join("; ")} }`);
    }
    if (hasBody) paramsSig.push("body: any");

    const callArgs = [];
    if (item.method === "GET") {
      if ((item.op.parameters || []).some((p) => p.in === "query")) {
        callArgs.push(`{ params }`);
      }
    } else if (hasBody && hasParamsInPath) {
      callArgs.push("body");
    } else if (hasBody) {
      callArgs.push("body");
    }

    const urlStr = hasParamsInPath ? "`" + pathFinal + "`" : `"${item.path}"`;
    const axiosCall =
      item.method === "GET"
        ? `api.get<${ret}>(${urlStr}${callArgs.length ? ", " + callArgs.join(", ") : ""})`
        : `api.${item.method.toLowerCase()}<${ret}>(${urlStr}${hasBody ? ", body" : ""}${item.method==="GET"?"":""})`;

    lines.push(`export async function ${fname}(api: AxiosInstance${paramsSig.length ? ", " + paramsSig.join(", ") : ""}) { return ${axiosCall}; }`);
  }
  fs.writeFileSync(path.join(outDir, `${group}.ts`), lines.join("\n") + "\n");
}

// Barrel file
const barrel = Object.keys(groups).map(g => `export * from "./${g}";`).join("\n");
fs.writeFileSync(path.join(outDir, "index.ts"), barrel + "\n");

console.log("Generated axios wrappers from:", path.relative(projectRoot, openapiPath));
