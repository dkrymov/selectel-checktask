import datetime
import memcache
import psycopg2

import grottybpm


class Doer(object):

    def __init__(self):
        self._db_connection = psycopg2.connect("user='postgres' host='db' password='' port='5432'")  # 192.168.222.138
        self._db_cursor = self._db_connection.cursor()

        self._mc = memcache.Client(['mem:11211'], debug=0)

    def __del__(self):
        self._db_connection.close()

    @staticmethod
    def date_beautify(unixtime):
        return datetime.datetime.utcfromtimestamp(unixtime).strftime("%c")

    def ticket_add(self, subject, body, email):
        # default_state = grottybpm.StateEngine()
        self._db_cursor.execute("INSERT INTO helpdesk.tickets (subject, body, email, status) VALUES (%s, %s, %s, %s)  RETURNING rn",
                                (subject, body, email, grottybpm.StateEngine().state.name))
        self._db_connection.commit()
        return self._db_cursor.fetchone()[0]

    def ticket_comment_add(self, ticket_id, body, email):
        self._db_cursor.execute("INSERT INTO helpdesk.comments (prn, body, email) VALUES (%s, %s, %s)",
                                (ticket_id, body, email))
        self._db_connection.commit()
        self._mc.delete("ticket_%s" % ticket_id)

    def ticket_get(self, ticket_id):

        value = self._mc.get("ticket_%s" % ticket_id)
        if value is not None:
            return value

        self._db_cursor.execute("select * from helpdesk.tickets where rn = %s", [ticket_id])
        ticket = self._db_cursor.fetchone()
        if ticket is None:
            return None
        else:
            self._db_cursor.execute("select cdate, email, body from helpdesk.comments where prn = %s", [ticket_id])
            comments = self._db_cursor.fetchall()

            result = {
                'ID':       ticket[0],
                'Created':  Doer.date_beautify(ticket[1]),
                'Modified': Doer.date_beautify(ticket[2]),
                'Subject':  ticket[3],
                'Contents': ticket[4],
                'Email':    ticket[5],
                'Status':   ticket[6]
            }

            if comments is not None:
                result['Comments'] = []
                for comment in comments:
                    result['Comments'].append({
                        'Created':  Doer.date_beautify(comment[0]),
                        'Contents': comment[2],
                        'Email':    comment[1]
                    })

            self._mc.set("ticket_%s" % ticket_id, result)

            return result

    def ticket_state_set(self, ticket_id, status):
        self._db_cursor.execute("select \"status\" from helpdesk.tickets where rn = %s", [ticket_id])
        ticket = self._db_cursor.fetchone()
        if ticket is None:
            return None
        else:
            bpm = grottybpm.StateEngine(ticket[0])
            if bpm.change(status):
                self._db_cursor.execute("update helpdesk.tickets set status = %s where rn = %s", (status, ticket_id))
                self._db_connection.commit()
                self._mc.delete("ticket_%s" % ticket_id)
                return True
            else:
                raise Exception('Status could not be changed')
