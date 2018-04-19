SELECT
    e.id,
    e.orgid,
    e.brandid,
    e.contactname,
    e.orderno,
    e.activestate,
    e.deactivedate,
    e.userid,
    e.updatedate
FROM entries e 
WHERE
    e.orgid = @orgid
    and e.brandid = @brandid
    /*@cond_contactname@*/
    /*@cond_activeflag@*/
/*@order_by@*/
