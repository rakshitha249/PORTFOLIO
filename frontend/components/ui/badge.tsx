import * as React from "react"

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "outline"
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  let classes = "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 "
  if (variant === "default") classes += "border-transparent bg-[var(--primary)] text-[var(--primary-foreground)] hover:opacity-80 "
  if (variant === "secondary") classes += "border-transparent bg-[var(--secondary)] text-[var(--secondary-foreground)] hover:opacity-80 "
  if (variant === "outline") classes += "text-[var(--foreground)] "
  
  return (
    <div className={`${classes} ${className || ""}`} {...props} />
  )
}

export { Badge }
