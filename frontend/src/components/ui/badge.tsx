import * as React from "react";
import { cn } from "@/lib/utils";

interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "destructive" | "outline";
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <div
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
        {
          "border-primary/40 bg-primary/15 text-primary hover:bg-primary/25":
            variant === "default",
          "border-border bg-secondary text-secondary-foreground hover:bg-secondary/80":
            variant === "secondary",
          "border-destructive/40 bg-destructive/15 text-destructive hover:bg-destructive/25":
            variant === "destructive",
          "text-foreground border-border/70 bg-card/60": variant === "outline",
        },
        className
      )}
      {...props}
    />
  );
}

export { Badge };