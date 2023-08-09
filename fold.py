import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

class fold2d:
    def __init__(self):
        plt.rcParams['text.color'] = (140 / 255, 140 / 255, 250 / 255)
        plt.rcParams['font.family'] = 'Courier New'
        
        self.num_points = 22
        self.x = np.linspace(-5, 5, self.num_points)
        self.y = np.linspace(-5, 5, self.num_points)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.grid = np.stack((self.X, self.Y), axis=-1)
        
        self.theta = 3.14159
        self.shear = 0
        
        self.create_plots()
    
    def update_transformation(self, val):
        self.theta = self.theta_slider.val
        self.shear = self.shear_slider.val
        
        # Associative, order doesn't matter
        transformed_grid = np.matmul(self.grid, np.array([[1, self.shear], [0, 1]]).T)
        transformed_grid = np.matmul(transformed_grid, np.array([[np.cos(self.theta), -np.sin(self.theta)], [np.sin(self.theta), np.cos(self.theta)]]))
        
        self.ax2.clear()
        scatter = self.ax2.scatter(transformed_grid[:,:,0], transformed_grid[:,:,1], color=(0.66, 0.66, 0.83), s=20)
        self.ax2.set_title(f'Rotation: {self.theta:.2f} rad\nShear: {self.shear:.2f}')
        
        self.update_matrices()
        plt.draw()
    
    def update_matrices(self):
        self.shear_matrix_display.set_text(f'Shear Matrix:\n[[1, {self.shear}]\n [0, 1]]')
        self.rotation_matrix_display.set_text(f'Rotation Matrix:\n[[{np.cos(self.theta):.2f}, {-np.sin(self.theta):.2f}]\n [{np.sin(self.theta):.2f}, {np.cos(self.theta):.2f}]]')

        combined_mat = np.array([[np.cos(self.theta), -np.sin(self.theta)],
                                 [np.sin(self.theta), np.cos(self.theta)]]) @ np.array([[1, self.shear],
                                                                                            [0, 1]])
        self.combined_transformations.set_text(f'Combined Transformation:\n{np.around(combined_mat, 2)}')
        plt.draw()
    
    
    def create_plots(self):
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(1, 3, figsize=(15, 5))
        self.fig.set_facecolor((0 / 255, 22 / 255, 37 / 255))
        self.ax1.set_facecolor((0 / 255, 22 / 255, 37 / 255))
        self.ax2.set_facecolor((0 / 255, 22 / 255, 37 / 255))

        self.ax3.set_axis_off()
        self.ax3.set_xticklabels([])
        self.ax3.set_yticklabels([])

        self.ax1.scatter(self.X, self.Y, color=(0.5, 0.66, 0.25), s=20)

        self.ax2.set_title(f'Rotation: {self.theta:.2f} rad\nShear: {self.shear:.2f}')
        transformed_grid = np.matmul(self.grid, np.array([[1, self.shear], [0, 1]]).T)
        transformed_grid = np.matmul(transformed_grid, np.array([[np.cos(self.theta), -np.sin(self.theta)], [np.sin(self.theta), np.cos(self.theta)]]))
        self.scatter = self.ax2.scatter(transformed_grid[:,:,0], transformed_grid[:,:,1], color=(0.66, 0.66, 0.83), s=20)

        ax_slider_rot = plt.axes([0.15, 0.02, 0.65, 0.03], facecolor='white')
        ax_slider_shear = plt.axes([0.15, 0.06, 0.65, 0.03], facecolor='white')
        self.theta_slider = Slider(ax_slider_rot, 'Rotation', 0, 2 * np.pi, valinit=self.theta)
        self.shear_slider = Slider(ax_slider_shear, 'Shear', -20, 20, valinit=self.shear, valstep=1)
        self.theta_slider.on_changed(self.update_transformation)
        self.shear_slider.on_changed(self.update_transformation)

        ax_matrices = plt.axes([0.69, 0.1, 0.15, 0.8], facecolor=(0 / 255, 22 / 255, 37 / 255))
        ax_matrices.set_title('Transformation Matrices')
        ax_matrices.spines['top'].set_visible(False)
        ax_matrices.spines['bottom'].set_visible(False)
        ax_matrices.spines['left'].set_visible(False)
        ax_matrices.spines['right'].set_visible(False)

        self.shear_matrix_display = ax_matrices.annotate(
            f'Shear Matrix:\n[[1, {self.shear}]\n [0, 1]]', 
            xy=(0.05, 0.8),
            fontsize=10, color=(140 / 255, 140 / 255, 250 / 255))

        self.rotation_matrix_display = ax_matrices.annotate(
            f'Rotation Matrix:\n[[{np.cos(self.theta):.2f}, {-np.sin(self.theta):.2f}]\n [{np.sin(self.theta):.2f}, {np.cos(self.theta):.2f}]]', 
            xy=(0.05, 0.6),
            fontsize=10, color=(140 / 255, 140 / 255, 250 / 255))

        combined_mat = np.array([[np.cos(self.theta), -np.sin(self.theta)],
                                 [np.sin(self.theta), np.cos(self.theta)]]) @ np.array([[1, self.shear],
                                                                                            [0, 1]])
        self.combined_transformations = ax_matrices.annotate(
            f'Combined Transformation:\n{np.around(combined_mat, decimals=2)}', 
            xy=(0.05, 0.4),
            fontsize=10, color=(140 / 255, 140 / 255, 250 / 255))

        plt.tight_layout()
        plt.show()

app = fold2d()
