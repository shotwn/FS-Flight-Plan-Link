# Server API Referance

<!-- Load the latest Swagger UI code and style from npm using unpkg.com -->
<script src="https://unpkg.com/swagger-ui-dist@3.25.0/swagger-ui-bundle.js"></script>
<link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3.25.0/swagger-ui.css"/>
<title>Server API Reference</title>

<div id="swagger-ui"></div> <!-- Div to hold the UI component -->
<script>
    window.onload = function () {
        // Begin Swagger UI call region
        const ui = SwaggerUIBundle({
            url: "../../api/fslink.v1.yaml", //Location of Open API spec in the repo
            dom_id: '#swagger-ui',
            deepLinking: true,
            withCredentials: true,
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.SwaggerUIStandalonePreset
            ],
            plugins: [
                SwaggerUIBundle.plugins.DownloadUrl
            ],
            onComplete: function() {
                ui.preauthorizeBasic("basicAuth", "User", "1234");
            }
        })
        window.ui = ui
    }
</script>

