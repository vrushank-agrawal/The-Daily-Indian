def create_head() -> str:
    return """
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Newsletter</title>
        <style>

            p {
                margin: 10px 0;
            }

            hr {
                border: none;
                border-top: 2px solid #000000;
                margin: 1em 0;
            }

            .body-canvas {
                font-family: Roboto,Helvetica Neue,Helvetica,Arial,sans-serif;
                background-color: white;
                color: #000000;
                max-width: 100%;
            }

            .container {
                max-width: 600px;
                margin: 10px auto;
                padding: 20px;
            }

            .image {
                max-width: 100%;
                height: auto;
                margin-bottom: 20px;
            }

            .m-top-5 {
                margin-top: 5px !important;
            }

            .m-top-10 {
                margin-top: 10px !important;
            }

            .m-top-30 {
                margin-top: 30px !important;
            }

            .m-bottom-30 {
                margin-bottom: 30px !important;
            }

            .section-title {
                background-color: lightgreen;
                display: inline-block;
                margin: 0;
                margin-top: 10px;
                padding: 10px;
                word-wrap: break-word;
            }

            .section-text {
                background-color: whitesmoke;
                letter-spacing: normal;
                line-height: 27px;
                margin: auto;
                margin-top: 20px;
                max-width: 600px;
                padding: 10px 20px 30px;
            }

            .button {
                background-color: #007bff;
                color: #fff;
                display: inline-block;
                font-size: 12px;
                padding: 1px 6px;
                text-decoration: none;
            }

            .button:hover {
                background-color: #0069d9;
            }

            header.header{
            }

            h1.title {
                text-align: center;
                font-size: 60px;
            }

            ul.arrow {
                padding-inline-start: 5px;
                list-style-type: none;
            }

            ul.arrow li {
                position: relative;
                margin-left: 20px; /* Add space to handle the arrow position */
            }

            ul.arrow li::before {
                content: "\\2192";
                position: absolute;
                left: -20px; /* Position the arrow outside the margin */
                padding-right: 8px; /* Space between arrow and text */
            }

            footer .copyrights {
                text-align: center;
                font-size: 12px;
                margin-top: 30px;
                line-height: 12px;
            }

        </style>
    </head>
    """