import seaborn as sns 
import matplotlib.pyplot as plt 
import os

def roofline(df_jobs, peak_p, peak_mb, hue = None, save_path = None, format = "pdf"):
    # Create roofline with system peak performance
    x = list(range(100000))
    mem_line = list(map(lambda i: min(top_perf, mem_bandwidth*i), x))
    ridge_point = peak_p/peak_mb
    plt.text(2**-30, 2**-18, f"Peak memory bandwidth {peak_mb} GByte/s", rotation = 40)
    plt.text(2**-4, 1.5*top_perf, f"Peak performance {peak_p} Flops/s", rotation = "horizontal")
    plt.vlines(x=ridge_point, ymin = 0, ymax = top_perf, color="black", linestyle="dashed")
    plt.text(ridge_point/4, 2**-21, "Ridge point", rotation = "vertical")
    
    # Plot job data
    sns.scatterplot(data = df_jobs, x = "arithm_ints", y = "p", hue = hue)
    plt.plot(x, mem_line, color="black")
    plt.xscale("log", base=2)
    plt.yscale("log", base=2)
    plt.xlabel("Operational intensity (Flops/Byte)")
    plt.ylabel("Performance (GFlops/s)")
    plt.tight_layout()
    
    # Save/Show figure 
    if save_path:
        plt.savefig(os.path.join(save_path, f"roofline{f'_{hue}' if hue else ''}.{format}"), format = format)
    else:
        plt.show()
    plt.clf()
    