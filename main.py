import tkinter as tk
from tkinter import simpledialog, messagebox
import time


class TreeNode:
    def __init__(self, value, x, y):
        self.value = value
        self.left = None
        self.right = None
        self.x = x
        self.y = y
        self.tag = f"node_{id(self)}"




class TreeBuilderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Clickable Binary Tree Visualizer")

        self.canvas = tk.Canvas(master, width=800, height=600, bg="white")
        self.canvas.pack()

        self.speed_slider = tk.Scale(master, from_=100, to=2000, label="Animation Speed (ms)",
                                     orient=tk.HORIZONTAL)
        self.speed_slider.set(1000)
        self.speed_slider.pack()

        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.pack(pady=10)

        tk.Button(self.buttons_frame, text="Pre-order", command=lambda: self.animate("pre")).grid(row=0, column=0, padx=10)
        tk.Button(self.buttons_frame, text="In-order", command=lambda: self.animate("in")).grid(row=0, column=1, padx=10)
        tk.Button(self.buttons_frame, text="Post-order", command=lambda: self.animate("post")).grid(row=0, column=2, padx=10)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.nodes = []
        self.root = None
        def get_depth(self, node):
            def depth_rec(n):
                if n is None:
                    return 0
                return 1 + max(depth_rec(n.left), depth_rec(n.right))
            return depth_rec(node)


    def on_canvas_click(self, event):
        node = self.get_clicked_node(event.x, event.y)
        if node:
            self.add_children(node)
        elif not self.root:
            value = simpledialog.askstring("Add Root", "Enter root value:")
            if value:
                self.root = TreeNode(value, event.x, event.y)
                self.nodes.append(self.root)
                self.draw_tree()

    def get_clicked_node(self, x, y):
        for node in self.nodes:
            if abs(node.x - x) < 30 and abs(node.y - y) < 30:
                return node
        return None

    def add_children(self, node):
        def calculate_depth(node):
            if not node:
                return 0
            return 1 + max(calculate_depth(node.left), calculate_depth(node.right))

        tree_depth = calculate_depth(self.root)  
        base_spacing = 160  
        vertical_spacing = 80  

        horizontal_spacing = base_spacing // (2 ** (tree_depth - 1)) if tree_depth > 1 else base_spacing

        left_value = simpledialog.askstring("Add Left Child", f"Enter LEFT child of {node.value} (or leave blank):")
        if left_value:
            node.left = TreeNode(left_value, node.x - horizontal_spacing, node.y + vertical_spacing)
            self.nodes.append(node.left)

        right_value = simpledialog.askstring("Add Right Child", f"Enter RIGHT child of {node.value} (or leave blank):")
        if right_value:
            node.right = TreeNode(right_value, node.x + horizontal_spacing, node.y + vertical_spacing)
            self.nodes.append(node.right)

        self.draw_tree()

    def draw_tree(self):
        self.canvas.delete("all")
        for node in self.nodes:
            if node.left:
                self.canvas.create_line(node.x, node.y, node.left.x, node.left.y)
            if node.right:
                self.canvas.create_line(node.x, node.y, node.right.x, node.right.y)

        for node in self.nodes:
            self.canvas.create_oval(node.x - 20, node.y - 20, node.x + 20, node.y + 20,
                                    fill="lightblue", tags=f"oval_{node.tag}")
            self.canvas.create_text(node.x, node.y, text=node.value, tags=f"text_{node.tag}")


    def animate(self, order):
        if not self.root:
            messagebox.showwarning("No Tree", "Add a root node first.")
            return

        order_list = []
        if order == "pre":
            self.preorder(self.root, order_list)
        elif order == "in":
            self.inorder(self.root, order_list)
        elif order == "post":
            self.postorder(self.root, order_list)

        self.animate_nodes(order_list)

    def animate_nodes(self, order_list):
        def step(index):
            if index > 0:
                prev_node = order_list[index - 1]
                self.canvas.itemconfig(f"oval_{prev_node.tag}", fill="lightblue")
            if index < len(order_list):
                node = order_list[index]
                self.canvas.itemconfig(f"oval_{node.tag}", fill="lightcoral")
                self.canvas.tag_raise(f"text_{node.tag}")
                self.master.after(self.speed_slider.get(), lambda: step(index + 1))
        step(0)

        step(0)

    def preorder(self, node, order):
        if node:
            order.append(node)
            self.preorder(node.left, order)
            self.preorder(node.right, order)

    def inorder(self, node, order):
        if node:
            self.inorder(node.left, order)
            order.append(node)
            self.inorder(node.right, order)

    def postorder(self, node, order):
        if node:
            self.postorder(node.left, order)
            self.postorder(node.right, order)
            order.append(node)


if __name__ == "__main__":
    root = tk.Tk()
    app = TreeBuilderApp(root)
    root.mainloop()
