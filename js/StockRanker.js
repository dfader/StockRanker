$(document).ready( function () {
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
                    