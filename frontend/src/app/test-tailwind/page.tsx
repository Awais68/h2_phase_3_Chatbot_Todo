export default function TestTailwind() {
    return (
        <div className="min-h-screen bg-background flex items-center justify-center">
            <div className="max-w-4xl mx-auto p-8 space-y-8">
                <h1 className="text-4xl font-display font-bold text-primary">
                    Tailwind CSS v4 Test Page
                </h1>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-card p-6 rounded-lg border border-primary/20 hover:border-primary/40 transition-colors">
                        <h2 className="text-2xl font-bold text-primary mb-2">Primary Color</h2>
                        <p className="text-foreground/80">Testing custom primary color</p>
                    </div>

                    <div className="bg-card p-6 rounded-lg border border-secondary/20 hover:border-secondary/40 transition-colors">
                        <h2 className="text-2xl font-bold text-secondary mb-2">Secondary Color</h2>
                        <p className="text-foreground/80">Testing custom secondary color</p>
                    </div>

                    <div className="bg-card p-6 rounded-lg border border-accent/20 hover:border-accent/40 transition-colors">
                        <h2 className="text-2xl font-bold text-accent mb-2">Accent Color</h2>
                        <p className="text-foreground/80">Testing custom accent color</p>
                    </div>
                </div>

                <div className="bg-surface/50 p-6 rounded-lg border border-border">
                    <h3 className="text-xl font-mono text-success mb-4">Custom Theme Variables Working!</h3>
                    <ul className="space-y-2 text-muted-foreground">
                        <li>✅ Custom colors from @theme</li>
                        <li>✅ Custom fonts (display, mono)</li>
                        <li>✅ Background and surface colors</li>
                        <li>✅ Border colors with opacity</li>
                        <li>✅ Responsive utilities</li>
                    </ul>
                </div>

                <div className="flex gap-4">
                    <button className="bg-primary hover:bg-primary-hover text-background px-6 py-3 rounded-lg font-bold transition-colors">
                        Primary Button
                    </button>
                    <button className="bg-secondary hover:bg-secondary-hover text-background px-6 py-3 rounded-lg font-bold transition-colors">
                        Secondary Button
                    </button>
                    <button className="bg-accent hover:bg-accent-hover text-background px-6 py-3 rounded-lg font-bold transition-colors">
                        Accent Button
                    </button>
                </div>
            </div>
        </div>
    )
}
