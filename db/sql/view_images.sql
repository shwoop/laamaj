create view images as
select ws_id, ws_date, ws_user, ws_chan, ws_url, ws_localfile
from websites
where ws_localfile!=''
/
