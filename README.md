# QNET – Survey Network Adjustment Plugin for QGIS

**QNET** is a QGIS plugin for least-squares adjustment of surveying control networks. It supports free network adjustment and multiple weighting strategies, including **robust estimation techniques** capable of mitigating the influence of outliers.  
For each robust method, the **tuning constants** controlling outlier sensitivity can be customized to achieve optimal results.

After adjustment, results are loaded directly into QGIS as a **point vector layer** containing all adjusted coordinates and statistics for further analysis within the QGIS environment. The results can also be exported to a **text report file**.

All network adjustment calculations are performed using the open-source **[PySurv](https://github.com/mpredki99/pysurv/tree/main)** library, designed for surveyors and geomatics engineers.

---

## Download and Installation

### 1) Download the correct release

1. Go to **GitHub ▸ Repository ▸ Releases**
2. Releases follow naming format: **`QNET-v<PLUGIN VERSION>`**
3. Each release description lists the **QGIS version it was tested with**
4. Select the release matching your QGIS installation
5. Under **Assets**, download: **`Source Code (zip)`**

### 2) Install in QGIS

1. Open **QGIS**
2. Go to **Plugins ▸ Manage and Install Plugins...**
3. Select **Install from ZIP** tab
4. Choose the downloaded **`Source Code (zip)`** archive
5. Click **Install Plugin** button
6. Enable **QNET** from the **Installed** plugins list if needed

In case of any issues or you need help, see the **[Official QGIS Plugin Documentation](https://docs.qgis.org/3.34/en/docs/user_manual/plugins/plugins.html)**.

---

## Plugin Usage Overview

The QNET interface consists of the following functional sections:

- Input files import
- Weighting methods and free-adjustment configuration
- Report export
- QGIS output layer export

---

![QNET Window](/doc/Window.png?raw=true "QNET Window")

---

### Input Files

QNET requires **two CSV files** as input:

#### 1) Survey Measurements File

File containing the survey measurements. Must contain the following columns (mandatory + optional):

| Column | Description |
|--------|-------------|
| `stn_id` | **(required)** Station identifier |
| `stn_h` | Station height (m) |
| `trg_id` | **(required)** Target identifier |
| `trg_h` | Target height (m) |
| `sd`, `ssd` | Slope distance and its sigma (m) |
| `hd`, `shd` | Horizontal distance and its sigma (m) |
| `vd`, `svd` | Vertical distance and its sigma (m) |
| `dx`, `dy`, `dz` | GNSS vector components (m) |
| `sdx`, `sdy`, `sdz` | GNSS vector component sigmas (m) |
| `a`, `sa` | Azimuth and its sigma (grad) |
| `hz`, `shz` | Horizontal direction and its sigma (grad) |
| `vz`, `svz` | Zenithal vertical angle and its sigma (grad) |
| `vh`, `svh` | Horizontal vertical angle and its sigma (grad) |

#### 2) Control Points File

File containing the approximate control point coordinates. Must contain the following columns (mandatory + optional):

| Column | Description |
|--------|-------------|
| `id` | **(required)** Point identifier |
| `x`, `y`, `z` | Approximate coordinates (m) |
| `sx`, `sy`, `sz` | Sigma values (m) |

File paths are entered manually or selected using the **[...]** dialog buttons.

---

### Free Adjustment and Weighting Configuration

#### Free adjustment

To enable free adjustment, activate the corresponding checkbox.

In free adjustment, all external constraints are removed, which introduces additional degrees of freedom: translation, rotation, and scale. This results in a singular (non-invertible) normal equation matrix. To solve the system, internal constraints must be applied, either by adding an inner constraint matrix **R** or by using pseudo-inversion. QNET automatically constructs the **R** matrix or, if the ordinary method is selected, applies the pseudo-inverse approach.

With free adjustment, coordinate corrections are distributed among reference points according to their sigma values. If all sigma values are equal, corrections are evenly distributed. If sigma values differ, corrections are distributed in proportion to each reference point's weight, calculated as $1/\sigma^2$.

**Note:** Setting a sigma value to $-1$ assigns a weight of zero to that coordinate, excluding it from the internal constraints. This is useful if a reference point is unstable and should not influence the inner constraints of the network.

#### Weighting methods

QNET implements several weighting strategies that determine how weights are assigned to measurements (observations) and, during free adjustment, to reference points:

| Method | Description |
|--------|-------------|
| **Ordinary** | No weighting (all weights = $1$). |
| **Weighted** | Calculates weights as $1/\sigma^2$. Weights stay constant. |
| **Robust** | Weights are initially computed as $1/\sigma^2$, then iteratively updated based on residuals or coordinate corrections. To control the strength of outlier suppression, **tuning constant** values can be adjusted. When a robust method is selected, QNET automatically applies recommended theoretical values for these constants, which generally provide optimal results, but they may be modified if needed. |

---

### Report Export

When report export is enabled, the plugin generates a **.txt report file** containing:

- **General information:** convergence status, number of iterations, weighting methods used, applied inner constraints if any, network specification, residual sigma
- **Control point statistics:** approximate coordinates, applied corrections, adjusted coordinates, adjusted sigmas, error ellipses
- **Measurement statistics:** observed values, residuals, adjusted values, adjusted sigmas

Report path can be selected using the **[...]** dialog button - if no report path is selected the report will be stored in the **same directory as the control points file**.

---

### QGIS Output Layer Exportation

After successful adjustment, QNET creates a **QGIS point vector layer** containing all adjusted point parameters.

#### Temporary layer (default)

- Layer is created in memory
- Custom layer name may be set
- Default name **"Adjusted points"** will be used if no layer name provided

#### Saving layer to file

- Output may be saved as a **Shapefile (.shp)**
- File path is chosen via dialog when the option is enabled

---

### Testing the Plugin

Example datasets are available in the [**PySurv**]((https://github.com/mpredki99/pysurv)) repository:

📁 `Repository → sample data`

They can be used directly to verify:

- File format correctness
- Adjustment workflow
- Report and layer export functions

---

### References

- PySurv documentation
  https://github.com/mpredki99/pysurv
- Official QGIS documentation
  https://docs.qgis.org/latest/en/docs/index.html

---
