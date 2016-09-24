import sys
import traceback


def build_javascript_files(top_list, bottom_list):
    try:
        f = open('js/StockRanker.js', 'w')

        message = """$(document).ready( function () {
                        $('#top_list_table_id').DataTable({
                            select: true,
                            "order": [[ 2, "desc" ]]
                        });
                        $('#bottom_list_table_id').DataTable({
                            select: true,
                            "order": [[ 2, "asc" ]]
                        });
                        console.log( "document ready" );
                    } );
                    """

        f.write(message)
        f.close()
        return f.name

    except Exception as e:
        print 'Error building HTML file', e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
