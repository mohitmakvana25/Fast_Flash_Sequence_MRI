# %% S0. SETUP env
import MRzeroCore as mr0
import pypulseq as pp
import numpy as np
import torch
from matplotlib import pyplot as plt
import util

# makes the ex folder your working directory
import os
os.chdir(os.path.abspath(os.path.dirname(__file__)))

experiment_id = 'exE01_FLASH_2D'


# %% S1. SETUP sys

# choose the scanner limits
system = pp.Opts(
    max_grad=28, grad_unit='mT/m', max_slew=150, slew_unit='T/m/s',
    rf_ringdown_time=20e-6, rf_dead_time=0,
    adc_dead_time=0, grad_raster_time=50 * 10e-6
)


seq = pp.Sequence()

# Define FOV and resolution
fov = 220e-3
slice_thickness = 8e-3
sz = (32, 32)  # spin system size / resolution
Nread = 64  # frequency encoding steps/samples
Nphase = 64  # phase encoding steps/samples

# Define rf events
rf1 = pp.make_block_pulse(
    flip_angle=5 * np.pi / 180, duration=0.1e-3,delay=0,phase_offset=0,
    slice_thickness=slice_thickness, time_bw_product=2.5,
    system=system
)

# seq.add_block(rf1,gz)
# seq.add_block(gzr)
# phi=0*np.pi/180
zoom = 1
# Define other gradients and ADC events
gx = pp.make_trapezoid(channel='x',area=Nread / fov * zoom ,rise_time=0.00001, duration=1e-3, system=system)
main_area = gx.area
timing = gx.flat_time
print(timing)
adc = pp.make_adc(num_samples=Nread, duration=1e-3,  system=system)
gx_pre = pp.make_trapezoid(channel='x', area=-0.5*gx.area, duration=0.2e-3, rise_time=0.00001,system=system)
# gx_spoil = pp.make_trapezoid(channel='x', flat_area=0.1*gx.area, flat_time=0.1e-3,rise_time=0.00001, system=system)

rf_phase = 0
rf_inc = 0
rf_spoiling_inc = 117
t = 1e-3
# ======
# CONSTRUCT SEQUENCE
# ======
# rf_prep = pp.make_block_pulse(flip_angle=180 * np.pi / 180, duration=1e-3, system=system)
#seq.add_block(rf_prep)
#seq.add_block(pp.make_delay(2))
#seq.add_block(gx_spoil)
#seq.add_block(rf_prep)
#seq.add_block(pp.make_delay(0.5))
for ii in range(-Nphase // 2, Nphase // 2):  # e.g. -64:63
    rf1.phase_offset = rf_phase / 180 * np.pi   # set current rf phase

    adc.phase_offset = rf_phase / 180 * np.pi  # follow with ADC

    rf_inc = divmod(rf_inc + rf_spoiling_inc, 360.0)[1]  # increase increment
    rf_phase = divmod(rf_phase + rf_inc, 360.0)[1]  # increment phase

    seq.add_block(rf1) 
    gy_pre = pp.make_trapezoid(channel='y', area=ii / fov * zoom, duration=0.2e-3,rise_time=0.00001, system=system)
    seq.add_block(gx_pre, gy_pre)

    gx = pp.make_extended_trapezoid(channel='x',amplitudes=np.array([0, main_area, main_area,2*main_area,2*main_area,0]), system=system, times=np.array([0, 0.5*t, 0.55*t, 0.58*t, 0.65*t, 0.75*t]))

    seq.add_block(adc, gx)

    
  
    

# %% S3. CHECK, PLOT and WRITE the sequence  as .seq
# Check whether the timing of the sequence is correct
ok, error_report = seq.check_timing()
if ok:
    print('Timing check passed successfully')
else:
    print('Timing check failed. Error listing follows:')
    [print(e) for e in error_report]

# PLOT sequence
sp_adc, t_adc = util.pulseq_plot(seq, clear=False, figid=(11,12))

# Prepare the sequence output for the scanner
seq.set_definition('FOV', [fov, fov, slice_thickness])
seq.set_definition('Name', 'gre')
seq.write('out/external.seq')
seq.write('out/' + experiment_id + '.seq')


# %% S4: SETUP SPIN SYSTEM/object on which we can run the MR sequence external.seq from above
sz = [64, 64]

if 1:
    # (i) load a phantom object from file
    # obj_p = mr0.VoxelGridPhantom.load_mat('../data/phantom2D.mat')
    obj_p = mr0.VoxelGridPhantom.load_mat('../data/numerical_brain_cropped.mat')
    obj_p = obj_p.interpolate(sz[0], sz[1], 1)
    # Manipulate loaded data
    obj_p.T2dash[:] = 30e-3
    obj_p.D *= 0 
    obj_p.B0 *= 0    # alter the B0 inhomogeneity
    # Store PD for comparison
    PD = obj_p.PD
    B0 = obj_p.B0
else:
    # or (ii) set phantom  manually to a pixel phantom. Coordinate system is [-0.5, 0.5]^3
    obj_p = mr0.CustomVoxelPhantom(
        pos=[[-0.4, -0.4, 0], [-0.4, -0.2, 0], [-0.3, -0.2, 0], [-0.2, -0.2, 0], [-0.1, -0.2, 0]],
        PD=[1.0, 1.0, 0.5, 0.5, 0.5],
        T1=1.0,
        T2=0.1,
        T2dash=0.1,
        D=0.0,
        B0=0,
        voxel_size=0.1,
        voxel_shape="box"
    )
    # Store PD for comparison
    PD = obj_p.generate_PD_map()
    B0 = torch.zeros_like(PD)

# obj_p.plot()
obj_p.size=torch.tensor([fov, fov, slice_thickness]) 
# Convert Phantom into simulation data
obj_p = obj_p.build()


# %% S5:. SIMULATE  the external.seq file and add acquired signal to ADC plot

use_simulation = True

if use_simulation:
    seq0 = mr0.Sequence.import_file("out/external.seq")
    seq0.plot_kspace_trajectory()
    graph = mr0.compute_graph(seq0, obj_p, 200, 1e-3)
    signal = mr0.execute_graph(graph, seq0, obj_p)
    spectrum = torch.reshape((signal), (Nphase, Nread)).clone().transpose(1, 0)
    kspace = spectrum
    # PLOT sequence with signal in the ADC subplot
    plt.close(11);plt.close(12)
    sp_adc, t_adc = mr0.util.pulseq_plot(seq, clear=False, signal=signal.numpy())
     

else:
    signal = mr0.util.get_signal_from_real_system('out/' + experiment_id + '.seq.dat', Nphase, Nread)
    spectrum = torch.reshape((signal), (Nphase, Nread, 20)).clone().transpose(1, 0)
    


# %% S6: MR IMAGE RECON of signal ::: #####################################

fig = plt.figure()  # fig.clf()
plt.subplot(411)
plt.title('ADC signal')
plt.plot(torch.real(signal), label='real')
plt.plot(torch.imag(signal), label='imag')


# this adds ticks at the correct position szread
major_ticks = np.arange(0, Nphase * Nread, Nread)
ax = plt.gca()
ax.set_xticks(major_ticks)
ax.grid()

space = torch.zeros_like(spectrum)

# fftshift
spectrum = torch.fft.fftshift(spectrum, 0)
spectrum = torch.fft.fftshift(spectrum, 1)
# FFT
space = torch.fft.fft2(spectrum, dim=(0, 1))
# fftshift
space = torch.fft.fftshift(space, 0)
space = torch.fft.fftshift(space, 1)

if use_simulation==False:
    space = torch.sum(space.abs(), 2)

plt.subplot(345)
plt.title('k-space')
mr0.util.imshow(np.abs(kspace.numpy()))
plt.subplot(349)
plt.title('k-space_r')
mr0.util.imshow(np.log(np.abs(kspace.numpy())))

plt.subplot(346)
plt.title('FFT-magnitude')
mr0.util.imshow(np.abs(space.numpy()),vmin=0)
plt.colorbar()
plt.subplot(3, 4, 10)
plt.title('FFT-phase')
mr0.util.imshow(np.angle(space.numpy()), vmin=-np.pi, vmax=np.pi)
plt.colorbar()

# % compare with original phantom obj_p.PD
plt.subplot(348)
plt.title('phantom PD')
mr0.util.imshow(obj_p.recover().PD.squeeze())
plt.subplot(3, 4, 12)
plt.title('phantom B0')
mr0.util.imshow(obj_p.recover().B0.squeeze())