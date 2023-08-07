import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, TextBox
from matplotlib.animation import FuncAnimation

plt.rcParams['text.color'] = (140 / 255, 140 / 255, 250 / 255)
plt.rcParams['font.family'] = 'Courier New'

class VectorPlotter:
    def __init__(self):
        self.v1 = np.array([1, 0, 0])
        self.v2 = np.array([0, 1, 0])

        self.fig = plt.figure()
        self.fig.set_facecolor((0 / 255, 22 / 255, 37 / 255)) # BG color fig

        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor((0 / 255, 22 / 255, 37 / 255)) # BG color axes area

        # Sliders and text boxes (bottom)
        axcolor = (90 / 255, 90 / 255, 90 / 255)
        self.ax_v1 = plt.axes([0.2, 0.07, 0.65, 0.03], facecolor=axcolor)
        self.ax_v2 = plt.axes([0.2, 0.03, 0.65, 0.03], facecolor=axcolor)
        
        self.ax_v1_input = plt.axes([0.085, 0.14, 0.25, 0.03])
        self.ax_v2_input = plt.axes([0.085, 0.19, 0.25, 0.03])

        self.s_v2 = Slider(self.ax_v2, 'Scalar v2', -9.0, 9.0, valinit=1.0)
        self.s_v1 = Slider(self.ax_v1, 'Scalar v1', -9.0, 9.0, valinit=1.0)

        self.v2_box = TextBox(self.ax_v1_input, 'v1:', initial=', '.join(map(str, self.v1)))
        self.v1_box = TextBox(self.ax_v2_input, 'v2:', initial=', '.join(map(str, self.v2)))

        self.s_v1.on_changed(self.update)
        self.s_v2.on_changed(self.update)
        self.v1_box.on_submit(self.enter_v1)
        self.v2_box.on_submit(self.enter_v2)

        plt.subplots_adjust(bottom=0.25)

        self.update(None)

    def update(self, val):

        # Get current values of the sliders
        scalar_v1 = self.s_v1.val
        scalar_v2 = self.s_v2.val

        # Update vector
        new_v1 = scalar_v1 * self.v1
        new_v2 = scalar_v2 * self.v2

        # Clear the previous plot
        self.ax.clear()

        span = new_v1 + new_v2
        cross_product = np.cross(new_v1, new_v2)

        if np.allclose(cross_product, [0, 0, 0]):
            self.ax.quiver(0, 0, 0, *new_v1, color='red')
            self.ax.quiver(0, 0, 0, *new_v2, color='blue')
            lims = np.max(np.abs(np.array([new_v1, new_v2]))) + 1
            self.ax.set_xlim([-lims, lims])
            self.ax.set_ylim([-lims, lims])
            self.ax.set_zlim([-lims, lims])
        else:
            normal = cross_product / np.linalg.norm(cross_product)
            d = -np.dot(normal, new_v1)
            xx, yy = np.meshgrid(np.linspace(-10, 10, 10), np.linspace(-10, 10, 10))
            zz = (-normal[0] * xx - normal[1] * yy - d) * 1.0 / normal[2]
            self.ax.plot_surface(xx, yy, zz, alpha=0.5, cmap='YlGn')
            self.ax.quiver(0, 0, 0, *new_v1, color='red')
            self.ax.quiver(0, 0, 0, *new_v2, color='blue')

            self.ax.set_xlim([-10, 10])
            self.ax.set_ylim([-10, 10])
            self.ax.set_zlim([-10, 10])

        # Clear the previous annotations #TODO: doesn't fully clear v1 annotation
        for annotation in self.fig.texts:
            annotation.remove()
          
        new_v1_rounded = np.round(new_v1, 3)
        new_v2_rounded = np.round(new_v2, 3)

        # Display values of v1 and v2 as annotations above the axes
        self.fig.text(0.17, 0.88, f"v1: {new_v1_rounded}", fontsize=10, color=(240/255,90/255,90/255))
        self.fig.text(0.17, 0.85, f"v2: {new_v2_rounded}", fontsize=10, color=(120/255,140/255,230/255))

        self.ax.set_axis_off()

        plt.grid()

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

if __name__ == "__main__":
    vector_plotter = VectorPlotter()
    plt.show()