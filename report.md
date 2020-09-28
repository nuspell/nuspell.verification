## Verification test results


The results below are measured on 73 dictionaries for very large word lists. Word frequency histograms of text typically have a long tail, hence speedup maximum is also reported on. Nuspell is more thorough than Hunspell and infrequent compounded words  result sometimes in a lower average speedup. Frequently  used words however have a much higher speedup.


| metric | average | minimum | maximum |
|--------|--------:|--------:|--------:|
| Accuracy        | 0.998 | 0.907 | 1.000 |
| Precision       | 1.000 | 1.000 | 1.000 |
| Speedup         | 1.2 | 0.4 | 2.5 |
| Speedup Maximum | 55.0 | 4.3 | 506.9 |

| speedup | speedup max. | dictionary | package | accuracy |
|--------:|-------------:|------------|---------|---------:|
| 2.5 | 22.9 | [bo](verification/hunspell-bo_0.4.0-1=bo.out)| bo_0.4.0-1  | 1.000 |
| 2.3 | 4.3 | [dz](verification/hunspell-dz_0.1.0-1=dz.out)| dz_0.1.0-1  | 1.000 |
| 2.2 | 198.2 | [sv_SE](verification/hunspell-sv_1%253a6.4.3-1=sv_SE.out)| sv_1%3a6.4.3-1  | 1.000 |
| 2.0 | 26.1 | [fr](verification/hunspell-fr-comprehensive_1%253a6.4.1-1=fr.out)| fr-comprehensive_1%3a6.4.1-1  | 1.000 |
| 2.0 | 21.5 | [fr](verification/hunspell-fr-classical_1%253a6.4.1-1=fr.out)| fr-classical_1%3a6.4.1-1  | 1.000 |
| 1.9 | 31.7 | [fr](verification/hunspell-fr-modern_1%253a6.4.1-1=fr.out)| fr-modern_1%3a6.4.1-1  | 1.000 |
| 1.8 | 29.0 | [fr](verification/hunspell-fr-revised_1%253a6.4.1-1=fr.out)| fr-revised_1%3a6.4.1-1  | 1.000 |
| 1.8 | 44.1 | [ro_RO](verification/hunspell-ro_1%253a6.4.3-1=ro_RO.out)| ro_1%3a6.4.3-1  | 1.000 |
| 1.8 | 68.8 | [ar](verification/hunspell-ar_3.2-1.1=ar.out)| ar_3.2-1.1  | 1.000 |
| 1.8 | 17.2 | [vi_VN](verification/hunspell-vi_1%253a6.4.3-1=vi_VN.out)| vi_1%3a6.4.3-1  | 1.000 |
| 1.8 | 127.1 | [te_IN](verification/hunspell-te_1%253a6.4.3-1=te_IN.out)| te_1%3a6.4.3-1  | 1.000 |
| 1.7 | 37.2 | [sk_SK](verification/hunspell-sk_1%253a6.4.3-1=sk_SK.out)| sk_1%3a6.4.3-1  | 1.000 |
| 1.7 | 315.1 | [bn_BD](verification/hunspell-bn_1%253a6.4.3-1=bn_BD.out)| bn_1%3a6.4.3-1  | 1.000 |
| 1.7 | 16.6 | [lo_LA](verification/hunspell-lo_1%253a6.4.3-1=lo_LA.out)| lo_1%3a6.4.3-1  | 1.000 |
| 1.7 | 28.6 | [ca_ES-valencia](verification/hunspell-ca_3.0.4+repack1-1=ca_ES-valencia.out)| ca_3.0.4+repack1-1  | 1.000 |
| 1.7 | 37.5 | [br_FR](verification/hunspell-br_0.12-2=br_FR.out)| br_0.12-2  | 1.000 |
| 1.7 | 20.1 | [lv_LV](verification/hunspell-lv_1.4.0-1=lv_LV.out)| lv_1.4.0-1  | 1.000 |
| 1.7 | 14.3 | [kmr_Latn](verification/hunspell-kmr_1%253a6.4.3-1=kmr_Latn.out)| kmr_1%3a6.4.3-1  | 1.000 |
| 1.7 | 14.3 | [hi_IN](verification/hunspell-hi_1%253a6.4.3-1=hi_IN.out)| hi_1%3a6.4.3-1  | 1.000 |
| 1.7 | 127.7 | [is_IS](verification/hunspell-is_1%253a6.4.3-1=is_IS.out)| is_1%3a6.4.3-1  | 1.000 |
| 1.7 | 48.5 | [af_ZA](verification/hunspell-af_1%253a6.4.3-1=af_ZA.out)| af_1%3a6.4.3-1  | 1.000 |
| 1.7 | 30.6 | [he_IL](verification/hunspell-he_1%253a6.4.3-1=he_IL.out)| he_1%3a6.4.3-1  | 1.000 |
| 1.7 | 33.5 | [gu_IN](verification/hunspell-gu_1%253a6.4.3-1=gu_IN.out)| gu_1%3a6.4.3-1  | 1.000 |
| 1.7 | 58.5 | [th_TH](verification/hunspell-th_1%253a6.4.3-1=th_TH.out)| th_1%3a6.4.3-1  | 1.000 |
| 1.7 | 506.9 | [uz_UZ](verification/hunspell-uz_0.6-4=uz_UZ.out)| uz_0.6-4  | 1.000 |
| 1.7 | 19.1 | [be_BY](verification/hunspell-be_0.53-3=be_BY.out)| be_0.53-3  | 1.000 |
| 1.7 | 14.3 | [tlh](verification/hunspell-tlh_1.0.7=tlh.out)| tlh_1.0.7  | 1.000 |
| 1.7 | 25.3 | [ne_NP](verification/hunspell-ne_1%253a6.4.3-1=ne_NP.out)| ne_1%3a6.4.3-1  | 1.000 |
| 1.7 | 16.6 | [si_LK](verification/hunspell-si_1%253a6.4.3-1=si_LK.out)| si_1%3a6.4.3-1  | 1.000 |
| 1.7 | 26.8 | [gug_PY](verification/hunspell-gug_1%253a6.4.3-1=gug_PY.out)| gug_1%3a6.4.3-1  | 1.000 |
| 1.6 | 37.0 | [ml_IN](verification/hunspell-ml_0.1-2=ml_IN.out)| ml_0.1-2  | 1.000 |
| 1.6 | 107.7 | [tr_TR](verification/hunspell-tr_1%253a6.4.3-1=tr_TR.out)| tr_1%3a6.4.3-1  | 0.986 |
| 1.3 | 46.3 | [ru_RU](verification/hunspell-ru_1%253a6.4.3-1=ru_RU.out)| ru_1%3a6.4.3-1  | 1.000 |
| 1.2 | 40.4 | [kk_KZ](verification/hunspell-kk_1.1-2=kk_KZ.out)| kk_1.1-2  | 0.907 |
| 1.2 | 135.2 | [sv_FI](verification/hunspell-sv_1%253a6.4.3-1=sv_FI.out)| sv_1%3a6.4.3-1  | 1.000 |
| 1.1 | 69.6 | [uk_UA](verification/hunspell-uk_1%253a6.4.3-1=uk_UA.out)| uk_1%3a6.4.3-1  | 1.000 |
| 1.1 | 152.0 | [nb_NO](verification/hunspell-no_1%253a6.4.3-1=nb_NO.out)| no_1%3a6.4.3-1  | 1.000 |
| 1.1 | 10.8 | [en_AU](verification/hunspell-en-au_1%253a2018.04.16-1=en_AU.out)| en-au_1%3a2018.04.16-1  | 1.000 |
| 1.1 | 15.3 | [tlh_Latn](verification/hunspell-tlh_1.0.7=tlh_Latn.out)| tlh_1.0.7  | 1.000 |
| 1.0 | 22.6 | [gd_GB](verification/hunspell-gd_1%253a6.4.3-1=gd_GB.out)| gd_1%3a6.4.3-1  | 1.000 |
| 1.0 | 121.4 | [nn_NO](verification/hunspell-no_1%253a6.4.3-1=nn_NO.out)| no_1%3a6.4.3-1  | 1.000 |
| 0.9 | 9.2 | [ko](verification/hunspell-ko_0.7.92-1=ko.out)| ko_0.7.92-1  | 1.000 |
| 0.9 | 16.3 | [sl_SI](verification/hunspell-sl_1%253a6.4.3-1=sl_SI.out)| sl_1%3a6.4.3-1  | 1.000 |
| 0.9 | 79.5 | [en_CA](verification/hunspell-en-ca_1%253a2018.04.16-1=en_CA.out)| en-ca_1%3a2018.04.16-1  | 1.000 |
| 0.9 | 13.0 | [en_US](verification/hunspell-en-us_1%253a2018.04.16-1=en_US.out)| en-us_1%3a2018.04.16-1  | 1.000 |
| 0.9 | 24.8 | [lt_LT](verification/hunspell-lt_1%253a6.4.3-1=lt_LT.out)| lt_1%3a6.4.3-1  | 1.000 |
| 0.9 | 28.3 | [cs_CZ](verification/hunspell-cs_1%253a6.4.3-1=cs_CZ.out)| cs_1%3a6.4.3-1  | 1.000 |
| 0.9 | 25.5 | [bs_BA](verification/hunspell-bs_1%253a6.4.3-1=bs_BA.out)| bs_1%3a6.4.3-1  | 1.000 |
| 0.8 | 16.1 | [en_ZA](verification/hunspell-en-za_1%253a6.4.3-1=en_ZA.out)| en-za_1%3a6.4.3-1  | 1.000 |
| 0.8 | 21.3 | [id_ID](verification/hunspell-id_1%253a6.4.3-1=id_ID.out)| id_1%3a6.4.3-1  | 1.000 |
| 0.8 | 10.5 | [an_ES](verification/hunspell-an_0.2-4=an_ES.out)| an_0.2-4  | 1.000 |
| 0.8 | 50.9 | [oc_FR](verification/hunspell-oc_1%253a6.4.3-1=oc_FR.out)| oc_1%3a6.4.3-1  | 1.000 |
| 0.8 | 40.3 | [nl](verification/hunspell-nl_2%253a2.10-6=nl.out)| nl_2%3a2.10-6  | 1.000 |
| 0.8 | 41.3 | [sw_TZ](verification/hunspell-sw_1%253a6.4.3-1=sw_TZ.out)| sw_1%3a6.4.3-1  | 1.000 |
| 0.8 | 82.8 | [bg_BG](verification/hunspell-bg_1%253a6.4.3-1=bg_BG.out)| bg_1%3a6.4.3-1  | 1.000 |
| 0.8 | 46.7 | [eu](verification/hunspell-eu_0.5.20151110-5=eu.out)| eu_0.5.20151110-5  | 1.000 |
| 0.8 | 42.1 | [ca](verification/hunspell-ca_3.0.4+repack1-1=ca.out)| ca_3.0.4+repack1-1  | 1.000 |
| 0.7 | 69.1 | [el_GR](verification/hunspell-el_1%253a6.4.3-1=el_GR.out)| el_1%3a6.4.3-1  | 1.000 |
| 0.7 | 31.5 | [pt_PT](verification/hunspell-pt-pt_1%253a6.4.3-1=pt_PT.out)| pt-pt_1%3a6.4.3-1  | 1.000 |
| 0.7 | 14.2 | [hr_HR](verification/hunspell-hr_1%253a6.4.3-1=hr_HR.out)| hr_1%3a6.4.3-1  | 1.000 |
| 0.7 | 54.7 | [en_GB](verification/hunspell-en-gb_1%253a6.4.3-1=en_GB.out)| en-gb_1%3a6.4.3-1  | 1.000 |
| 0.6 | 36.5 | [es_ES](verification/hunspell-es_1%253a6.4.3-1=es_ES.out)| es_1%3a6.4.3-1  | 1.000 |
| 0.6 | 25.4 | [gl_ES](verification/hunspell-gl_1%253a6.4.3-1=gl_ES.out)| gl_1%3a6.4.3-1  | 1.000 |
| 0.6 | 13.3 | [it_IT](verification/hunspell-it_1%253a6.4.3-1=it_IT.out)| it_1%3a6.4.3-1  | 1.000 |
| 0.6 | 32.1 | [pl_PL](verification/hunspell-pl_1%253a6.4.3-1=pl_PL.out)| pl_1%3a6.4.3-1  | 1.000 |
| 0.5 | 22.3 | [de_CH_frami](verification/hunspell-de-ch-frami_1%253a6.4.3-1=de_CH_frami.out)| de-ch-frami_1%3a6.4.3-1  | 1.000 |
| 0.5 | 43.0 | [de_DE_frami](verification/hunspell-de-de-frami_1%253a6.4.3-1=de_DE_frami.out)| de-de-frami_1%3a6.4.3-1  | 1.000 |
| 0.5 | 16.5 | [de_DE](verification/hunspell-de-de_20161207-7=de_DE.out)| de-de_20161207-7  | 1.000 |
| 0.5 | 21.5 | [de_CH](verification/hunspell-de-ch_20161207-7=de_CH.out)| de-ch_20161207-7  | 1.000 |
| 0.5 | 247.1 | [da_DK](verification/hunspell-da_1%253a6.4.3-1=da_DK.out)| da_1%3a6.4.3-1  | 0.997 |
| 0.4 | 16.4 | [de_AT_frami](verification/hunspell-de-at-frami_1%253a6.4.3-1=de_AT_frami.out)| de-at-frami_1%3a6.4.3-1  | 1.000 |
| 0.4 | 42.2 | [de_AT](verification/hunspell-de-at_20161207-7=de_AT.out)| de-at_20161207-7  | 1.000 |
| 0.4 | 39.2 | [se](verification/hunspell-se_1.0~beta6.20081222-1.2=se.out)| se_1.0~beta6.20081222-1.2  | 1.000 |
