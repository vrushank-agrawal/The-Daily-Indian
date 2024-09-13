def create_head() -> str:
    return """
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Newsletter</title>
        <style>

            p {{
                margin: 10px 0;
            }}

            hr {{
                border: none;
                border-top: 2px solid #ccc;
                margin: 10px 0;
                border-radius: 50px;
            }}

            .body-canvas {{
                font-family: Arial, sans-serif;
                background-color: beige;
                color: #333;
                margin: 30px auto;
                padding: 30px 60px;
                border-radius: 10px;
                max-width: 780px;
            }}

            .container {{
                max-width: 600px;
                margin: 10px auto;
                padding: 20px;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}

            .image {{
                max-width: 100%;
                height: auto;
                margin-bottom: 20px;
            }}

            .section-title {{
            }}

            .section {{
            }}

            .button {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #007bff;
                color: #fff;
                text-decoration: none;
                border-radius: 4px;
            }}

            .button:hover {{
                background-color: #0069d9;
            }}

            header.header{{
            }}

            h1.title {{
                text-align: center;
                margin-top: 0;
                font-size: 60px;
            }}

            ul.arrow {{
                padding-inline-start: 5px;
                list-style-type: none;
            }}

            ul.arrow li::before {{
                content: "\\2192";
                padding-right: 8px;
            }}

            footer .copyrights {{
                text-align: center;
                font-size: 12px;
                margin-top: 20px;
            }}

        </style>
    </head>
    """