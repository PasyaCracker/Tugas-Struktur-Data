import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

class GameOfLife:
    def __init__(self, rows=50, cols=50):
        """
        Inisialisasi Game of Life
        
        Parameters:
        rows: jumlah baris grid
        cols: jumlah kolom grid
        """
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        
    def set_pattern(self, pattern, position=(0, 0)):
        """
        Menempatkan pola pada grid
        
        Parameters:
        pattern: array 2D dari pola yang ingin ditempatkan
        position: tuple (row, col) untuk posisi kiri atas pola
        """
        rows, cols = pattern.shape
        r, c = position
        self.grid[r:r+rows, c:c+cols] = pattern
        
    def random_pattern(self, density=0.3):
        """
        Membuat pola acak
        
        Parameters:
        density: kepadatan sel hidup (0.0 - 1.0)
        """
        self.grid = np.random.choice([0, 1], size=(self.rows, self.cols), 
                                     p=[1-density, density])
        
    def count_neighbors(self, row, col):
        """
        Menghitung jumlah tetangga hidup di sekitar sel
        """
        # Menghitung tetangga dengan mempertimbangkan batas grid
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                r = (row + i) % self.rows
                c = (col + j) % self.cols
                count += self.grid[r, c]
        return count
    
    def next_generation(self):
        """
        Menghitung generasi berikutnya berdasarkan aturan Game of Life
        """
        new_grid = np.zeros((self.rows, self.cols), dtype=int)
        
        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = self.count_neighbors(i, j)
                
                # Aturan 1: Sel hidup dengan 2-3 tetangga tetap hidup
                if self.grid[i, j] == 1 and neighbors in [2, 3]:
                    new_grid[i, j] = 1
                
                # Aturan 2 & 3: Sel hidup dengan <2 atau >3 tetangga mati
                # (sudah dihandle karena default new_grid adalah 0)
                
                # Aturan 4: Sel mati dengan tepat 3 tetangga menjadi hidup
                elif self.grid[i, j] == 0 and neighbors == 3:
                    new_grid[i, j] = 1
        
        self.grid = new_grid
        
    def run_interactive(self, generations=100, interval=200):
        """
        Menjalankan simulasi dengan visualisasi animasi
        
        Parameters:
        generations: jumlah generasi maksimum
        interval: delay antar frame dalam milidetik
        """
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Colormap: putih untuk mati, hitam untuk hidup
        cmap = ListedColormap(['white', 'black'])
        
        img = ax.imshow(self.grid, cmap=cmap, interpolation='nearest')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title('Conway\'s Game of Life - Generasi 0')
        
        generation_count = [0]
        
        def update(frame):
            self.next_generation()
            img.set_array(self.grid)
            generation_count[0] += 1
            ax.set_title(f'Conway\'s Game of Life - Generasi {generation_count[0]}')
            return [img]
        
        anim = animation.FuncAnimation(fig, update, frames=generations,
                                      interval=interval, blit=True, repeat=False)
        plt.show()
        
    def print_grid(self):
        """
        Mencetak grid ke console
        """
        for row in self.grid:
            print(' '.join(['■' if cell else '·' for cell in row]))
        print()


# ========== POLA-POLA TERKENAL ==========

# Pola stabil (Still lifes)
BLOCK = np.array([
    [1, 1],
    [1, 1]
])

BEEHIVE = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
])

# Pola osilator (Oscillators)
BLINKER = np.array([
    [1, 1, 1]
])

TOAD = np.array([
    [0, 1, 1, 1],
    [1, 1, 1, 0]
])

PULSAR = np.array([
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]
])

# Pola bergerak (Spaceships)
GLIDER = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1]
])

LWSS = np.array([  # Lightweight Spaceship
    [0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0]
])

# Pola dari contoh di soal
EXAMPLE_1 = np.array([
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0]
])

EXAMPLE_STABLE = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
])


# ========== CONTOH PENGGUNAAN ==========

def demo_1():
    """Demo 1: Pola acak"""
    print("Demo 1: Pola Acak")
    game = GameOfLife(50, 50)
    game.random_pattern(density=0.3)
    game.run_interactive(generations=200, interval=100)

def demo_2():
    """Demo 2: Glider - pola yang bergerak"""
    print("Demo 2: Glider (Pola Bergerak)")
    game = GameOfLife(30, 30)
    game.set_pattern(GLIDER, position=(5, 5))
    game.run_interactive(generations=100, interval=200)

def demo_3():
    """Demo 3: Pulsar - osilator periodik"""
    print("Demo 3: Pulsar (Osilator)")
    game = GameOfLife(40, 40)
    game.set_pattern(PULSAR, position=(13, 13))
    game.run_interactive(generations=50, interval=300)

def demo_4():
    """Demo 4: Multiple patterns"""
    print("Demo 4: Berbagai Pola")
    game = GameOfLife(60, 60)
    game.set_pattern(GLIDER, position=(5, 5))
    game.set_pattern(BLINKER, position=(20, 20))
    game.set_pattern(BLOCK, position=(40, 40))
    game.set_pattern(TOAD, position=(30, 15))
    game.run_interactive(generations=150, interval=150)

def demo_5():
    """Demo 5: Contoh dari soal"""
    print("Demo 5: Contoh dari Soal")
    game = GameOfLife(20, 20)
    game.set_pattern(EXAMPLE_1, position=(8, 8))
    
    print("Generasi 0:")
    game.print_grid()
    
    game.next_generation()
    print("Generasi 1:")
    game.print_grid()
    
    game.next_generation()
    print("Generasi 2:")
    game.print_grid()

def demo_6():
    """Demo 6: Pola stabil dari soal"""
    print("Demo 6: Pola Stabil")
    game = GameOfLife(20, 20)
    game.set_pattern(EXAMPLE_STABLE, position=(8, 8))
    game.run_interactive(generations=30, interval=500)


if __name__ == "__main__":
    print("=" * 60)
    print("CONWAY'S GAME OF LIFE")
    print("=" * 60)
    print("\nPilih demo yang ingin dijalankan:")
    print("1. Pola Acak")
    print("2. Glider (Pola Bergerak)")
    print("3. Pulsar (Osilator)")
    print("4. Berbagai Pola Sekaligus")
    print("5. Contoh dari Soal (Console)")
    print("6. Pola Stabil dari Soal")
    print()
    
    choice = input("Pilihan (1-6): ")
    
    if choice == '1':
        demo_1()
    elif choice == '2':
        demo_2()
    elif choice == '3':
        demo_3()
    elif choice == '4':
        demo_4()
    elif choice == '5':
        demo_5()
    elif choice == '6':
        demo_6()
    else:
        print("Pilihan tidak valid. Menjalankan demo pola acak...")
        demo_1()