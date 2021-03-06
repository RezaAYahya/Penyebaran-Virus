import random
import matplotlib.pyplot as plt
from celluloid import Camera as Camera

"""
TUBES MOSI PENYEBARAN VIRUS
Anggota Kelompk:
Imaduddin M. Fadhil / 1301184115
M. Faishal Darma Putra / 1301183483
Reza Ahmad Yahya / 1301184403
"""


# POINT 1
# Inisialisasi variable scalar :
jumlahIndividu = 200
rasioInfeksi = 0.05  # 5%
probMove = 0.8  # 80%
pemulihan = 10  # dalam satuan hari
totalInfeksi = []
infeksiSementara = int(jumlahIndividu * rasioInfeksi)
# Ukuran Ruang Simulasi
x_min = 0
x_max = 20
y_min = 0
y_max = 20
x_range = x_max - x_min
y_range = y_max - y_min
x_pos = []
y_pos = []
x_infeksi = [0]
y_infeksi = [0]
x_sehat = [0]
y_sehat = [0]

# POINT 2
# Inisialisasi Variable List :
statusInfeksi = []
statusImun = []
waktuInfeksi = []
# Inisialisasi Posisi
for i in range(jumlahIndividu):
    x_pos.append(random.randint(x_min, x_max))
    y_pos.append(random.randint(y_min, y_max))
    # Inisialisasi Status Kesehatan
    if (i < infeksiSementara):
        statusInfeksi.append(True)
    else:
        statusInfeksi.append(False)
    # Inisialisasi Status Imunitas
    statusImun.append(False)
    # Inisialisasi Waktu Terinfeksi
    waktuInfeksi.append(0)


# POINT 3
# Update Posisi
def posisi(x, y):
    posisiRandom = random.random()
    if (posisiRandom <= 0.2):
        x = x + 1
    elif (posisiRandom <= 0.4):
        y = y - 1
    elif (posisiRandom <= 0.6):
        x = x - 1
    elif (posisiRandom <= 0.8):
        y = y + 1
    return [x, y]


# Koreksi Posisi Dengan PBC
# a. Correction X axis
def pbc(x, y):
    if (x > x_max):
        x = x - x_range
    elif (x < x_min):
        x = x + x_range
    # b. Correction Y axis
    elif (y > y_max):
        y = y - y_range
    elif (y < y_min):
        y = y + y_range
    return [x, y]


# Jarak individu sehat = individu terinfeksi
def posisiSama(x, y, x_pos, y_pos):
    status = False
    i = 0
    while ((status == False) & (i < jumlahIndividu)):
        if ((statusInfeksi[i]) & (x_pos[i] == x) & (y_pos[i] == y)):
            status = True
        i = i + 1
    return status


Camera = Camera(plt.figure())
hari = 0
# Iterasi
while (infeksiSementara > 0):
    hari += 1
    for j in range(jumlahIndividu):
        # Update posisi berdasarkan probabilitas individu bergerak
        randProb = random.uniform(0,1)
        if(randProb >= probMove):
            updatePosisi = posisi(x_pos[j], y_pos[j])
        else:
            updatePosisi = [x_pos[j], y_pos[j]]
            
        # Koreksi dengan PBC
        koreksi = pbc(updatePosisi[0], updatePosisi[1])

        # Update Waktu Terinfeksi Individu
        if (statusInfeksi[j]):
            waktuInfeksi[j] = waktuInfeksi[j] + 1

        # Update status kesehatan individu - recovery
        if (waktuInfeksi[j] >= pemulihan):
            statusImun[j] = True
            statusInfeksi[j] = False
            waktuInfeksi[j] = 0
            infeksiSementara = infeksiSementara - 1

        # Update status kesehatan individu – infection
        if (~statusImun[j] & ~statusInfeksi[j] & posisiSama(koreksi[0], koreksi[1], x_pos, y_pos)):
            statusInfeksi[j] = True
            infeksiSementara = infeksiSementara + 1

        # Update posisi terbaru
        x_pos[j] = koreksi[0]
        y_pos[j] = koreksi[1]

        # pos = [x_pos[j], y_pos[j]]
        if (statusInfeksi[j]):
            x_infeksi.append(x_pos[j])
            y_infeksi.append(y_pos[j])
        else:
            x_sehat.append(x_pos[j])
            y_sehat.append(y_pos[j])

    # Perubahan infeksi
    totalInfeksi.append(infeksiSementara)
    # Plotting
    plt.figure(1)
    plt.subplot(1, 2, 1)
    plt.scatter(x_sehat, y_sehat, c="green", s=25)
    plt.scatter(x_infeksi,y_infeksi, c="red", s=25)
    plt.title("Simulasi Random Walk Penyebaran Virus")
    plt.subplot(1, 2, 2)
    plt.plot(totalInfeksi, c='blue')
    Camera.snap()
    
    x_infeksi = []
    y_infeksi = []
    x_sehat = []
    y_sehat = []

# Animasi
anim = Camera.animate(interval=1000)
plt.grid(True, which="both")
plt.legend()
plt.title("Grafik Penyebaran Virus")
plt.xlabel('Jumlah Hari')
plt.ylabel('Jumlah Terinfeksi')
plt.show()
