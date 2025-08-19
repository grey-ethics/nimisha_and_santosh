/**
 * Tiny form inputs.
 */
import React from "react";

export const Input = (props: React.InputHTMLAttributes<HTMLInputElement>) => (
  <input {...props} className={`w-full px-3 py-2 rounded-lg border ${props.className ?? ""}`} />
);

export const Select = (props: React.SelectHTMLAttributes<HTMLSelectElement>) => (
  <select {...props} className={`w-full px-3 py-2 rounded-lg border bg-white ${props.className ?? ""}`} />
);

export const Textarea = (props: React.TextareaHTMLAttributes<HTMLTextAreaElement>) => (
  <textarea {...props} className={`w-full px-3 py-2 rounded-lg border ${props.className ?? ""}`}/>
);

export const Label = ({ children }: { children: React.ReactNode }) => (
  <label className="text-sm text-gray-600">{children}</label>
);

export const Button = ({ children, ...rest }: React.ButtonHTMLAttributes<HTMLButtonElement>) => (
  <button {...rest} className={`px-4 py-2 rounded-xl shadow border bg-white hover:bg-gray-50 text-sm ${rest.className ?? ""}`}>
    {children}
  </button>
);

export const Primary = ({ children, ...rest }: React.ButtonHTMLAttributes<HTMLButtonElement>) => (
  <button {...rest} className={`px-4 py-2 rounded-xl shadow bg-blue-600 text-white hover:bg-blue-700 text-sm ${rest.className ?? ""}`}>
    {children}
  </button>
);
