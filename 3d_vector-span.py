import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox, Button

plt.rcParams['text.color'] = (140 / 255, 140 / 255, 250 / 255)
plt.rcParams['font.family'] = 'Courier New'

class VectorPlotter:
    def __init__(self):
        self.v1 = np.array([1, 0, 0])
        self.v2 = np.array([0, 1, 0])
        self.span_plane_visible = True
        self.span_3d_visible = False
        # self.ints_only = True #TODO

        self.fig = plt.figure()
        self.fig.set_facecolor((0 / 255, 22 / 255, 37 / 255)) # BG color fig

        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor((0 / 255, 22 / 255, 37 / 255)) # BG color axes area

        # Sliders and text boxes (bottom) TODO: issue with refresh (issue in update method)
        axcolor = (90 / 255, 90 / 255, 90 / 255)
        self.ax_v1 = plt.axes([0.2, 0.07, 0.65, 0.03], facecolor=axcolor)
        self.ax_v2 = plt.axes([0.2, 0.03, 0.65, 0.03], facecolor=axcolor)
        
        self.ax_v1_input = plt.axes([0.085, 0.19, 0.25, 0.03])
        self.ax_v2_input = plt.axes([0.085, 0.14, 0.25, 0.03])

        self.s_v2 = Slider(self.ax_v2, 'Scalar v2', -10.0, 10.0, valinit=10.0, valstep=1)
        self.s_v1 = Slider(self.ax_v1, 'Scalar v1', -10.0, 10.0, valinit=10.0, valstep=1)

        self.v2_box = TextBox(self.ax_v1_input, 'v1:', initial=', '.join(map(str, self.v1)))
        self.v1_box = TextBox(self.ax_v2_input, 'v2:', initial=', '.join(map(str, self.v2)))

        self.s_v1.on_changed(self.update)
        self.s_v2.on_changed(self.update)
        self.v1_box.on_submit(self.enter_v1)
        self.v2_box.on_submit(self.enter_v2)

        # Button - Show/Hide span
        self.ax_button = plt.axes([0.8, 0.12, 0.1, 0.04], frame_on=False)
        self.button = Button(self.ax_button, 'Show/Hide span')
        self.button.on_clicked(self.toggle_span)

        self.ax_button_3d = plt.axes([0.8, 0.16, 0.1, 0.04], frame_on=False)
        self.button = Button(self.ax_button_3d, 'Show/Hide 3D')
        self.button.on_clicked(self.toggle_span_3d)


        plt.subplots_adjust(bottom=0.05)

        self.ax.view_init(elev=20, azim=-45)
        #self.ax.mouse_init(rotate_btn=3)

    def update(self, val):
        # Clear the previous plot
        self.ax.clear()

        # Get current values of the sliders
        scalar_v1 = self.s_v1.val
        scalar_v2 = self.s_v2.val

        # Update vector
        new_v1 = scalar_v1 * self.v1
        new_v2 = scalar_v2 * self.v2

        self.ax.set_xlim([-10, 10])
        self.ax.set_ylim([-10, 10])
        self.ax.set_zlim([-10, 10])

        self.ax.quiver(0, 0, 0, *new_v1, color=(1, 0, 0))
        self.ax.quiver(0, 0, 0, *new_v2, color=(0, 0, 1))

        # Clear the previous annotations #TODO: doesn't fully clear v1 annotation
        for annotation in self.fig.texts:
            annotation.remove()

        # self.fig.text(0.1, 0.76, f"Cross product: None", fontsize=10, color=(190/255, 190/255, 190/255))
        # self.fig.text(0.125, 0.73, f"Determinant: None", fontsize=10, color=(190/255, 190/255, 190/255))

        # Show the linear combination v1 & v2
        linear_combination = None

        if not np.allclose(new_v1, [0, 0, 0]) and not np.allclose(new_v2, [0, 0, 0]):
            combined = new_v1 + new_v2
            self.ax.quiver(0, 0, 0, *combined, color='green', linestyle='dotted')
            linear_combination = new_v1 + new_v2

        #TODO make class either round all to ints or none (see class self.ints_only)
        new_v1_rounded = np.round(new_v1, 1)
        new_v2_rounded = np.round(new_v2, 1)

        if (new_v1_rounded + new_v2_rounded != 0).any():
            linear_combination = new_v1_rounded+new_v2_rounded

        self.fig.text(0.035, 0.79, f"Linear combination: {linear_combination}", fontsize=10, color=(120/255, 230/255, 120/255))
        
        # Update vecor values rounded
        self.fig.text(0.1, 0.88, f"v1: {new_v1_rounded}", fontsize=10, color=(240/255, 90/255, 90/255))
        self.fig.text(0.1, 0.85, f"v2: {new_v2_rounded}", fontsize=10, color=(120/255, 140/255, 230/255))

        # Show the dot product of v1 & v2
        dot = None

        if np.dot(new_v1, new_v2) != 0:
            dot = np.dot(new_v1, new_v2)

        self.fig.text(0.125, 0.76, f"Dot product: {dot}", fontsize=10, color=(190/255, 190/255, 190/255))
        
        # Show span only when the button is pressed
        if self.span_plane_visible:
            print('Trying to create span')
            span = new_v1 + new_v2
            cross_product = np.cross(new_v1, new_v2)
            print(cross_product)

            if not np.allclose(cross_product, [0, 0, 0]):
                normal = cross_product / np.linalg.norm(cross_product)
                d = -np.dot(normal, new_v1)
                xx, yy = np.meshgrid(np.linspace(-10, 10, 10), np.linspace(-10, 10, 10))
                zz = (-normal[0] * xx - normal[1] * yy - d) * 1.0 / normal[2]
                self.ax.plot_surface(xx, yy, zz, alpha=0.5, cmap='YlGn')


        if not self.span_3d_visible:
            self.ax.set_axis_off()

    def enter_v1(self, text):
        try:
            self.v1 = np.array([float(val.strip()) for val in text.split(',')])
            self.update(None)
        except Exception as e:
            print(f"Invalid input for v1. Error: {e}")
            self.v1_box.set_val(', '.join(map(str, self.v1)))

    def enter_v2(self, text):
        try:
            self.v2 = np.array([float(val.strip()) for val in text.split(',')])
            self.update(None)
        except Exception as e:
            print(f"Invalid input for v2. Error: {e}")
            self.v2_box.set_val(', '.join(map(str, self.v2)))

    def toggle_span(self, event):
        print("2d span toggled")
        self.span_plane_visible = not self.span_plane_visible
        self.update(None)

    def toggle_span_3d(self, event):
        print("3d span toggled")
        self.span_3d_visible = not self.span_3d_visible
        self.update(None)

if __name__ == "__main__":
    vector_plotter = VectorPlotter()
    vector_plotter.update(None)
    plt.show()