import * as React from "react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "ghost" | "link";
  size?: "default" | "sm" | "lg" | "icon";
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => {
    let classes = "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 ";
    
    if (variant === "default") classes += "bg-[var(--primary)] text-[var(--primary-foreground)] hover:opacity-90 ";
    if (variant === "outline") classes += "border border-[var(--border)] bg-transparent hover:bg-[var(--accent)] hover:text-[var(--accent-foreground)] ";
    if (variant === "ghost") classes += "hover:bg-[var(--accent)] hover:text-[var(--accent-foreground)] ";
    if (variant === "link") classes += "text-[var(--primary)] underline-offset-4 hover:underline ";

    if (size === "default") classes += "h-9 px-4 py-2 ";
    if (size === "sm") classes += "h-8 rounded-md px-3 text-xs ";
    if (size === "lg") classes += "h-10 rounded-md px-8 ";
    if (size === "icon") classes += "h-9 w-9 ";

    return (
      <button ref={ref} className={`${classes} ${className || ""}`} {...props} />
    );
  }
);
Button.displayName = "Button";

export { Button };
