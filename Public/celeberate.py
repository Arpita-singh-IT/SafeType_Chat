import tkinter as tk
import random

class CelebrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown & Confetti")
        self.root.geometry("600x400")
        
        # 1. Setup Label for Countdown
        self.label = tk.Label(root, text="5", font=("Arial", 80), fg="blue")
        self.label.pack(expand=True)
        
        # 2. Setup Canvas for Confetti (hidden at first)
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.confetti_particles = []
        
        # Start the countdown
        self.counter = 5
        self.update_countdown()

    def update_countdown(self):
        if self.counter > 0:
            self.label.config(text=str(self.counter))
            self.counter -= 1
            # Wait 1000ms (1 second) then call this function again
            self.root.after(1000, self.update_countdown)
        else:
            self.show_confetti()

    def show_confetti(self):
        # Remove the countdown label and show the canvas
        self.label.pack_forget()
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_text(300, 200, text="SURPRISE!", font=("Arial", 40), fill="red")
        
        # Create 50 confetti pieces
        for _ in range(50):
            x = random.randint(0, 600)
            y = random.randint(0, 400)
            color = random.choice(["red", "blue", "yellow", "green", "purple", "orange"])
            p = self.canvas.create_oval(x, y, x+10, y+10, fill=color, outline="")
            self.confetti_particles.append(p)
        
        self.animate_confetti()

    def animate_confetti(self):
        for p in self.confetti_particles:
            self.canvas.move(p, random.randint(-2, 2), random.randint(1, 5))
        self.root.after(50, self.animate_confetti)

# Initialize the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CelebrationApp(root)
    root.mainloop()  # This line MUST be here to keep the window open!