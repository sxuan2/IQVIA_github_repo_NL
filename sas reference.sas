SAS REFERENCE

时间
%let todaysDate = %sysfunc(today(), yymmn4.);
%put &todaysDate.;
%let testmnd = %eval(&todaysDate. - 1);
%put &testmnd.;


一些乱七八糟的小工具
%macro export(dataset,name,location = output); proc export data = &dataset. outfile = "&dir.\&location.\&name..csv" replace; run; %mend;
%macro row_count(dataset); proc sql; select count(1) from &dataset.; quit; %mend;
%macro import_csv(name,address); 
proc import datafile = &address. out = &name. dbms = CSV replace; 
guessingrows=max;
run; 
%mend;
%macro fillwithzero(input, output, columns); data &output.; set &input.; array help &columns.; do over help; if help=. then help=0; end; run; %mend; 
%macro info(data=); proc contents data=&data.; run; %mend; 
%macro print(data=, obs=10); proc print data =&data.(obs=&obs.); run; %mend;

指定work到别的地方
libname temp "C:\Data\Janssen_Imbruvica\&study_to.";options user=temp;


proc summary data = dfd1 nway missing;
class  pat combi line;
var daily_dosage;
output out=dfd2(drop=_:) median(daily_dosage) =median_dd mean(daily_dosage)=avg_dd ;
run;
以上等同于
proc sql;
	create table dfd2 as
	select pat, combi, line, mean(daily_dosage), median(daily_dosage)
	from dfd1
	group by pat, combi, line;
quit;
但是sas里面 有时候没有median这个函数


填0
data mtd12; set mtd11; array help ara: cyp: pgp: both:; do over help; if help=. then help=0; end; run;

抹掉

data test1;
input var1 $ var2;
cards;
a 1
b 2
c 3
;
run;

data test2;
input var1 $ var2;
cards;
a 2
;
run;

proc sql;
	CREATE TABLE test3
	AS
	SELECT a.var1
		, CASE 
			WHEN b.var1 IS NOT NULL THEN b.var2
			ELSE a.var2
		END AS var2
	FROM test1 a
		LEFT JOIN test2 b ON a.var1 = b.var1;
quit;



多重left join
proc sql;
	CREATE TABLE pat_info_nbr_result
	AS
	SELECT a.*, b.indication AS indication_base_case, c.indication AS indication_scenario1, d.indication AS indication_scenario2
	FROM pat_info_nbr a
		LEFT JOIN indi_0 b ON a.pat = b.pat
		LEFT JOIN indi_12 c ON a.pat = c.pat
		LEFT JOIN indi_15 d ON a.pat = d.pat;
quit;



PROC SORT DATA = messy OUT = neat NODUPKEY DUPOUT = extraobs;
BY Family DESCENDING Length;
RUN;


DATA dataname;
SET dataname1(KEEP = Class Species);
run;

DATA dataname;
SET dataname1(RENAME = (Class=Ban Species=Zhong));
run;

PROC TRANSPOSE DATA = olddata OUT = newdata;
	BY a;
	ID b;
	VAR c;
RUN;

data gap_&dataset.;
informat lag_numdax DDMMYY10.;
format lag_numdax DDMMYY10.;
set info_&dataset.;
by pat;
lag_numdax = lag(numdax);	
if first.pat then gap = td;
else gap = lag_numdax - numdax;
daily_dosage = cutstr/gap;
run;

proc import datafile = '/folders/myfolders/SASCrunch/cars.csv'
 out = work.cars
 dbms = CSV
 ;
run;



#查是否一一对应
proc sql;
	create table check1 as
	select Onekey_Hospital_Name,count(*)as cnt 
	from 
		(select distinct Onekey_Hospital_Name, Parent_Wkp_Local_Onekey_ID from xbt_02_onekey)
	group by Onekey_Hospital_Name
	order by cnt desc;
quit;


dm 'log; file logfile replace';
dm 'output; file outfile replace';
%include "X:\Organisatie\Checklists\check log.sas";




proc datasets noprint; change XBT_01=XBT_01_test; quit;

options ls=120; proc freq data=knmp_raw; table atc4*line*prodplus*pack/list missing;run

maand= year(numdax)*100+month(numdax);


data focus_drug;
              set focus_drug_pret;
                            LOT=catx("+", of COL:);
                            IMATINIB_drug=(index(LOT, "IMATINIB")>0);
                            DASATINIB_drug=(index(LOT,"DASATINIB")>0);
                            NILOTINIB_drug=(index(LOT,"NILOTINIB")>0);
                            BOSUTINIB_drug=(index(LOT,"BOSUTINIB")>0);
                            keep pat IMATINIB_drug DASATINIB_drug NILOTINIB_drug BOSUTINIB_drug;
run;



proc datasets library=work nolist memtype=data kill;quit;


PROC SORT DATA=interest_rx
 DUPOUT=interest_rx_dups
 out = test NODUPRECS ;
 BY pat ;
RUN ;



如果丢失了phaid_BSN_list

proc sort data=PATREP.Patrep_total_202009 out=Patrep_total nodupkey;
            by patxpo;
        run;
/*data werk.Patrep_total; set Patrep_total; run;*/
proc sort data=PATREP.list_F13_phaid_202009(keep=phaid) out=phaid_BSN_list nodupkey;
    by phaid;
run;



%macro match_rate(input);
	proc sql;
		create table comparison_v1
		as
		select a.pat, a.indication as indication_new, b.indication as indication_ori
		from &input. a
		inner join deliverd_202002_result b
		on a.pat = b.pat
		where a.pat in (select distinct pat from pat_selected);
	quit;

	data comparison_v1_1;
	set comparison_v1;
	if indication_new=indication_ori;
	run;

	proc sql noprint;
	    select count(1) into: all1 from comparison_v1;
		select count(1) into: all2 from comparison_v1_1;
	quit;

	data _NULL_;
		haha = &all2./&all1.;
	    call symput("haha",haha);
	run;

	%put &haha.;
%mend;

%match_rate(RF_202009_v1);
%match_rate(RF_202009_v3);
%match_rate(rerun_202009);


%macro select_mono_usr(xbt_01,line,value,output);

	data _xbt_02;
		length &line.2 $ 100;
		set &xbt_01.;
		if index(&line., &value.) > 0 then &line.2 = "&value.";
		else &line.2 = &line.;
	run; 

	proc sql;
		create table _xbt_02_usr as
		select distinct pat
		from 
			(select * from _xbt_02 where &line.2 = "&value.");
	quit;

	proc sql;
		create table _mono_usr
		as
		select distinct pat, count(distinct &line.2) as n 
		from _xbt_02
		group by pat
		having n = 1;
	quit;

	proc sql;
		create table &output.
		as
		select distinct pat
		from _xbt_02_usr
		where pat in (select distinct pat from _mono_usr);
	quit;

%mend;

