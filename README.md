# To run the project

```
chmod +x run.sh </br>
./run.sh <br />
```

Following results will appear once the shell script is run.<br />

```

=======================================<br />
Generating results file with regular queries.................<br />
=======================================<br />
Gathered Pages<br />
Gathered Paragraphs<br />
Gathered Regular Queries<br />
Gathered Results<br />

=======================================<br />
Running evaluation framework.............<br />
=======================================<br />
runid	 all 	test<br />
num_q	 all 	60<br />
num_ret	 all 	2100<br />
num_rel_ret	 all 	174<br />
map	 all 	0.2295310245310245<br />
gm_map	 all 	0.6585904496408844<br />
Rpec	 all 	0.10599206349206347<br />
recip_rank	 all 	0.22433261183261183<br />
P_5	 all 	0.07<br />
P_10	 all 	0.04500000000000001<br />
P_15	 all 	0.03333333333333333<br />
P_20	 all 	0.026666666666666675<br />
P_30	 all 	0.018333333333333333<br />
P_100	 all 	0.005500000000000001<br />
P_200	 all 	0.0027500000000000007<br />
P_500	 all 	0.0011000000000000003<br />
P_1000	 all 	0.000550000000000000<br />
```

```
=======================================<br />
Generating results file with tagme enchanced queries.........<br />
=======================================<br />
Gathered Pages<br />
Gathered Paragraphs<br />
Generating TagMe enchanced queries........<br />
Gathered Tagme Enhanced Queries<br />
Gathered Results<br />
=======================================<br />
Running evaluation framework on results on tagme enhanced results<br />
=======================================<br />
runid	 all 	test<br />
num_q	 all 	60<br />
num_ret	 all 	2100<br />
num_rel_ret	 all 	174<br />
map	 all 	0.2079354904354904<br />
gm_map	 all 	0.6511606087084545<br />
Rpec	 all 	0.11154761904761905<br />
recip_rank	 all 	0.2138481888481888<br />
P_5	 all 	0.07666666666666667<br />
P_10	 all 	0.04666666666666667<br />
P_15	 all 	0.03333333333333333<br />
P_20	 all 	0.026666666666666675<br />
P_30	 all 	0.018333333333333333<br />
P_100	 all 	0.005500000000000001<br />
P_200	 all 	0.0027500000000000007<br />
P_500	 all 	0.0011000000000000005<br />
P_1000	 all 	0.0005500000000000002<br />
```
