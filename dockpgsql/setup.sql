CREATE SCHEMA helpdesk;
ALTER SCHEMA helpdesk OWNER TO postgres;
GRANT ALL ON SCHEMA helpdesk TO postgres;

CREATE table helpdesk.tickets (
    rn      int generated always AS IDENTITY primary key,
    cdate   int DEFAULT extract(epoch from now()),
    mdate   int DEFAULT extract(epoch from now()),
    subject varchar(255) not null,
    body    text not null,
    email   varchar(255) not null,
    status  varchar(127) not null
);

CREATE table helpdesk.comments (
    rn      int generated always AS IDENTITY primary key,
    prn     int not null REFERENCES helpdesk.tickets (rn) ON DELETE CASCADE,
    cdate   int DEFAULT extract(epoch from now()),
    email   varchar(255) not null,
    body    text not null
);

CREATE FUNCTION helpdesk.ticket_stamp() RETURNS trigger AS $ticket_stamp$
    BEGIN
        NEW.mdate := extract(epoch from now());
        RETURN NEW;
    END;
$ticket_stamp$ LANGUAGE plpgsql;

CREATE TRIGGER tickets_stamp BEFORE UPDATE ON helpdesk.tickets
    FOR EACH ROW EXECUTE PROCEDURE helpdesk.ticket_stamp();

CREATE FUNCTION helpdesk.ticket_comment_stamp() RETURNS trigger AS $ticket_comment_stamp$
    BEGIN
        update helpdesk.tickets set mdate = extract(epoch from now()) where rn = NEW.prn;
        RETURN NEW;
    END;
$ticket_comment_stamp$ LANGUAGE plpgsql;

CREATE TRIGGER tickets_comments_stamp AFTER INSERT ON helpdesk.comments
    FOR EACH ROW EXECUTE PROCEDURE helpdesk.ticket_comment_stamp();
