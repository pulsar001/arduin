#!/usr/bin/env python3

from flask import Flask, jsonify, request, url_for, redirect, session
app = Flask(__name__)

# This is the HTML, normally you would abstract it out into a template file and have Jinja render it
HTML = """
<!DOCTYPE html>
<html>
<head>
 <title>Continuous Update Demo</title>
 <!-- Pull in jQuery from Google-->
 <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
</head>

<body>
 <div>
   <h2>A continuously updated list:</h2>
   <ul id="culist">
   </ul>
 </div>

<script type="text/javascript">

function requestUpdate() {                         // 3

   console.log("DEBUG: requesting update");

   $.getJSON('/_refresh', function(result) {       // 4
      console.log("DEBUG: Received " + result.data);
      var HTML = "<li>" + result.data + "</li>";
      $("#culist").append(HTML);
   });

}

// This fires just once when the site initially loads
$(document).ready(function() {                      // 1
    console.log("DEBUG: document ready");
    // Get first element for list
    requestUpdate();
    // Ensure list is updated every 3s
    setInterval(requestUpdate, 3000);               // 2
});

</script>

</body>
</html>
"""

@app.route('/_refresh')                                # 5
def refresh():
    # print(request.args) to see what the Javascript sent to us
    print('DEBUG: Refresh requested');


    # Query your Thingspeak here and then pass the new data back to Javascript below


    # Build our response (a Python "dict") to send back to Javascript
    response =  { 
        'status' : 'Success', 
        'data': "A new line derived from Thingspeak",
    }
    print(f'DEBUG: Sending response {response}')
    return jsonify(response)                          # 6 - send the result to client


@app.route('/')
def main():
    print(f'DEBUG: Sending main page')
    return HTML

if __name__ == '__main__':
    app.run(debug=True)