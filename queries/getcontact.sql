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
    e.id = @cid
    and e.orgid = @orgid
    and e.brandid = @brandid
