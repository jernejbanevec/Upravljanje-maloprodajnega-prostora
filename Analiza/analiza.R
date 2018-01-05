require(reshape2)

st_produktov <- c(2:10)
povprecja_ds <- c(2252.311818408007, 3143.1831609044366, 4280.116962968127, 5541.585444746526, 6501.973186455406, 7530.25347214121, 8754.290465617662, 9786.694783226574, 10856.17098199368)
povprecja_ss <- c(2345.602636111844, 3207.5533302456315, 4256.5370910694555, 5199.690682474628, 5812.365118850423, 6896.47033920601, 7296.699005079152, 7921.030172898909, 8550.78511195774)

povprecja <- data.frame(st_produktov, povprecja_ds, povprecja_ss)
colnames(povprecja) <- c('st','ds','ss')

plot(povprecja$st, povprecja$ds, 'b', 
     main = 'Primerjava dobičkov strategij v odvisnosti od števila produktov',
     xlab = 'število produktov',
     ylab = 'dobiček',
     col = 'orange',
     lwd = 2)
lines(povprecja$st, povprecja$ss, 'b', add = TRUE,
     col = 'blue',
     lwd = 2)