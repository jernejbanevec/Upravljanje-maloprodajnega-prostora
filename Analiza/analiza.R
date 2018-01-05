require(reshape2)

#Generirava od 2 do 15 podatkov
st_produktov <- c(2:15)

#Doloèiva razliène C, da pozneje strategiji lahko primerjava tudi glede na ponudbo celotnega prostora, ki ga imamo na razpolago
C <- c(20.0, 32.0, 44.0, 56.0, 68.0, 80.0, 92.0, 104.0, 116.0, 128.0, 140.0)

#Podaktke generirava dvakrat za obe strategiji, obakrat za od 2 do 15 izdelkov, ter povpreèja izraèunava iz vzorca velikosti 150

povprecja_ds2 <- c(1570.4492053618771, 2594.0359927099594, 3312.7105366827827, 4165.512177465852, 5008.286648521151, 6019.373105010036, 6862.542727763537, 7771.1027920611905, 8233.333423108286, 9197.708207762675, 10328.078587034914, 11250.349882205286, 11641.207568570257, 12805.595715579124)
povprecja_ss2 <- c(914.1135052619471, 1515.5968932896749, 2082.353586581799, 2615.373000279465, 3400.076665979961, 3868.9451976764976, 4410.00945935456, 5116.067281899035, 5452.532912760001, 5752.143734433003, 7026.204444453788, 7599.368274323282, 7817.536072551987, 8436.661590499965)
povprecja_ds1 <- c(1719.1577306426695, 2472.1589359134377, 3399.167555096737, 4301.6845003199205, 5151.687498659725, 5906.5840465452175, 6773.21167930758, 7632.9892980918285, 8668.140869084396, 9450.588406396502, 10194.911349246117, 10944.232618969745, 11905.037689614675, 12915.327958299991)
povprecja_ss1 <- c(1016.2279002524145, 1484.1531737692326, 2204.6881729037987, 2739.0833039238764, 3365.982737104273, 3834.712505158931, 4447.288237539012, 5057.3628386094415, 5725.604341943888, 6238.999651653176, 6618.049730456601, 7109.921399522913, 7936.699208152525, 8513.192172812242)

povprecja_ds <- (povprecja_ds1 + povprecja_ds2)/2
povprecja_ss <- (povprecja_ss1 + povprecja_ss2)/2

prostor_ds <- c(2537.5245386934757, 3072.770704738585, 3501.448026972073, 3798.2808305709823, 3911.382635973741, 4034.8021775368406, 4082.425167439962, 4162.58025316439, 4433.059452144997, 4445.669129261109, 4398.244969231403) 
prostor_ss <- c(921.0312488957906, 1082.3619069709737, 1288.474736955253, 1604.5781398041308, 1775.550692910966, 2012.9074631754813, 2244.3210946441754, 2548.696103405482, 2825.3627029252766, 2968.6814084546377, 2964.7052280564503)

povprecja <- data.frame(st_produktov, povprecja_ds, povprecja_ss)
colnames(povprecja) <- c('st','ds','ss')

poraba <- data.frame(C, prostor_ds, prostor_ss)
colnames(poraba) <- c('C','ds','ss')

#Graf primerjave dobièkov obeh strategij v odvisnosti od števila produktov
plot(povprecja$st, povprecja$ds, 'b', 
     main = 'Primerjava dobièkov strategij v odvisnosti od števila produktov',
     xlab = 'število produktov',
     ylab = 'dobièek',
     ylim = c(0,13000),
     col = 'orange',
     lwd = 2)
lines(povprecja$st, povprecja$ss, 'b', #add = TRUE,
     col = 'blue',
     lwd = 2)
legend('bottomright', 
       legend = c('dodeljen prostor', 'skupen prostor'),
       col = c('orange', 'blue'),
       lwd = 1:1,
       bty = 'n')

#Graf primerjave dobièkov obeh strategij v odvisnosti od prostora
plot(poraba$C, poraba$ds, 'b', 
     main = 'Primerjava dobièkov strategij v odvisnosti od prostora',
     xlab = 'prostor',
     ylab = 'dobièek',
     col = 'red',
     lwd = 2,
     ylim=c(2500, 5000))
lines(poraba$C, poraba$ss, 'b', add = TRUE,
      col = 'green',
      lwd = 2)
legend('bottomright', 
       legend = c('dodeljen prostor', 'skupen prostor'),
       col = c('red', 'green'),
       lwd = 1:1,
       bty = 'n')

