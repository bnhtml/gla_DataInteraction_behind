桥接名称：数据目录  数据区：mysql  sql语句：select data_name$domain_name$first_name$second_name$third_name$interface_type$interface_name from dataname ;
桥接名称：服务目录  数据区：mysql  sql语句：select link_name$firstName$secondName$thirdName from servicedata ;
桥接名称：用户目录  数据区：mysql  sql语句：select username$api_key from user ;
桥接名称：访问控制目录  数据区：mysql  sql语句：select serviceName$acl$WhiteName from accesscontrol ;
桥接名称：流量控制目录  数据区：mysql  sql语句：select name$username$serviceName$user_day from flowcontrol ;
桥接名称：企业基本信息  数据区：大数据    sql语句：select UNISCID$ENTNAME$REGNO$ENTTYPE_CN$ESTDATE$INDUSTRYPHY$REGORG_CN$OPSCOTYPE_CN$OPSCOPE$OPFROM$OPTO$REGSTATE_CN$DOMDISTRICT$DOM$REGCAPCUR_CN$REGCAPUSD$RECCAPUSD$COUNTRY$EMPNUM$TOWN$NAME$REPORTTYPE$APPRDATE from FRK_LIB_SCHEMAS.e_baseinfo where UNISCID="%s" and ENTNAME="%s";
桥接名称：行政处罚信息  数据区：大数据    sql语句：select PENDECNO$ILLEGACTTYPE$PENTYPE$PENAM$FORFAM$PENCONTENT$PENAUTH_CN$PENDECISSDATE$PUBLICDATE from FRK_LIB_SCHEMAS.case_pub_baseinfo where PENDECNO="%s";
桥接名称：企业异常名录详细信息  数据区：大数据  sql语句：select UNISCID$ENTNAME$REGNO$LEREP$CERTYPE$CERNO$SPECAUSE$SPECAUSE_CN$DECORG_CN$ISMOVE$REMEXCPRES_CN$REMDATE$REDECORG_CN from FRK_LIB_SCHEMAS.ao_opa_detail where UNISCID="%s" and ENTNAME="%s";
桥接名称：行政处罚当事人信息  数据区：大数据  sql语句：select CASEPARTYID$NAME$GTREGNO$UNITNAME$UNISCID$REGNO$LEREP from FRK_LIB_SCHEMAS.case_pub_partyinfo where UNISCID="%s" and  LEREP="%s";
桥接名称：严重违法失信企业详细信息  数据区：大数据  sql语句：select ENTNAME$UNISCID$REGNO$NAME$CERTYPE$CERNO$SERILLREA_CN$ABNTIME$DECORG_CN$DEDOCNUM$REMEXCPRES_CN$REMDATE$RECORG_CN$REDOCNUM from FRK_LIB_SCHEMAS.e_li_illdisdetail where CERNO="%s" and ENTNAME="%s" and NAME="%s";
桥接名称：股权冻结被执行人信息  数据区：大数据  sql语句：select UNISCID$ENTNAME$REGNO$FROAUTH$EXECUTENO$INV$FROAM$REGCAPCUR_CN$FROZSTATE_CN$PUBLICDATE from FRK_LIB_SCHEMAS.e_sf_partyinfo where UNISCID="%s" and INV="%s";
桥接名称：其他部门公示_行政处罚信息  数据区：大数据  sql语句：select UNISCID$ENTNAME$REGNO$PENDECNO$ILLEGACTTYPE$PENTYPE_CN$PENAM$FORFAM$PENCONTENT$JUDAUTH$PENDECISSDATE$REMARK$PUBLICDATE from FRK_LIB_SCHEMAS.e_ot_case where UNISCID="%s" and ENTNAME="%s";
桥接名称：证件查询  数据区：大数据  sql语句：select PENTYPE$ILLEGACTTYPE from FRK_LIB_SCHEMAS.
case_pub_baseinfo;
桥接名称：证件查询  数据区：大数据  sql语句：select PENTYPE$ILLEGACTTYPE from FRK_LIB_SCHEMAS.
case_pub_baseinfo;
桥接名称：证件查询  数据区：大数据  sql语句：select PENTYPE$ILLEGACTTYPE from FRK_LIB_SCHEMAS.case_pub_baseinfo;
桥接名称：测试系统  数据区：mysql  sql语句：select 222$334 from 11 ;
桥接名称：ww  数据区：mysql  sql语句：select 222$334 from 11 ;
桥接名称：wwdwadaw  数据区：mysql  sql语句：select 222$334 from 11 ;
桥接名称：fg  数据区：mysql  sql语句：select 222$334 from 11 ;
�Ž����ƣ�wqd  ��������mysql  sql��䣺select name_user from test ;
�Ž����ƣ�gdg  ��������mysql  sql��䣺select name_user from test ;
�Ž����ƣ�eeeee  ��������mysql  sql��䣺select wefwef from wwww ;
桥接名称：低保个人信息查询  数据区：易鲸捷  sql语句：select SPEOPNAME$SIDCARD$SSEXNAME$SWORKABLENAME$STDJZDXNAME from MZT_GZ_SCHEMAS.peopleinfo where SPEOPNAME="%s" and SIDCARD="%s" ;
桥接名称：低保家庭信息查询  数据区：易鲸捷  sql语句：select SPEOPLES$SSHINAME$SSHICODE$STOWNNAME$STOWNCODE$SVILLAGENAME$SVILLAGECODE$SIDCARD$SPEOPNAME$SSFNY$SJTLBNAME$SJTLBCODE$SLBNAME$SLBCODE$SFAMILYNO$FBZJE from MZT_GZ_SCHEMAS.d2_peopleinfo where SPEOPNAME="%s" and SIDCARD="%s" ;
桥接名称：低保家庭信息查询  数据区：易鲸捷  sql语句：select SPEOPLES$SSHINAME$SSHICODE$STOWNNAME$STOWNCODE$SVILLAGENAME$SVILLAGECODE$SIDCARD$SPEOPNAME$SSFNY$SJTLBNAME$SJTLBCODE$SLBNAME$SLBCODE$SFAMILYNO$FBZJE from MZT_GZ_SCHEMAS.d2_peopleinfo where SPEOPNAME="%s" and SIDCARD="%s" ;
