# TODO: Add comment
# 
# Author: jlehtoma
###############################################################################

x = 1:7
if (exists("avdia.koivu")) {
	xmod = 5.0
	scale = 4.0
	mod.asym = 0.9
	transformed.koivu = transform.sigmoidal(avdia.koivu)
	koivu = avdia.koivu[seq(1, length(avdia.koivu), 1000)]
}
if (exists("avdia.kuusi")) {
	kuusi = avdia.kuusi[seq(1, length(avdia.kuusi), 1000)]
}
if (exists("avdia.manty")) {
	manty = avdia.manty[seq(1, length(avdia.manty), 1000)]
}
if (exists("avdia.muulp")) {
	mlp = avdia.muulp[seq(1, length(avdia.muulp), 1000)]
}

data = list(koivu, kuusi, manty, mlp)

gr.device()
parop <- par(mfcol=c(2, 2))

for (y. in data) {
	x. <- 1:length(y.)
	plot(x., y.)
	data <- curve(splinefun(x., y., method="mono")(x), add=TRUE, n = 200)
	#browser()
}
