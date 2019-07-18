Zhang et al 2019
-------------------------------------------------------------------

Image Quality:
Format = TIFF
Resolution = 3264x2448 pixels
bit = 8bit

-------------------------------------------------------------------
LithoGraphX(1.2.0) parameters pipeline:


Import Stack:
	Channel = 2
	Time Point = 1

Main - Transfer function editor:
	Scale Gray
		Manual Adjustment to enhance cell wall/lumen contrast

Process – Stack - Filters
	Apply Transfer Function:
		Red = 0
		Green = 0
		Blue = 0
		Alpha = 1
	Gaussian Blur Stack:
		X Sigma (µm) = 0.25
		Y Sigma (µm) = 0.25
		Z Sigma (µm) = 0.0
Process – Stack – Morphology
	Sieve Filter:
		Type = Median
		Size (µm2/µm2) = 1
		Fully Connected = No

Process – Stack – Segmentation
	Segment Section:
		BlurX = 0.3
		BlurY = 0.3
		nBlur = 1
		WatershedLevel = 1500
		ApplyTransferFct = True
		Invert = Yes
Process – Mesh – Cell Mesh:
	Cell Mesh From 2D Image:
		Edge Length (µm) = 0.1
		Z Slice = 0
		Show Errors with Mesh = Yes









