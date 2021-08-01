/**
 *
 * CovXray Javascript
 * This file deals with uploading user x-ray scans and 
 * communicating with server and presenting results.
 *
 * @author Akhil Kokani
 */

class CovXray {

    constructor() {
        this.csrf_token = $("input[name=csrfmiddlewaretoken]");
        this.scanning_animation = $("div.scanning-animation");
        this.xray_scan_preview = $("div.xray-scan-preview");
        this.xray_image = $("input#xray-image");
        this.scan_btn = $("button#scan_xray");
        this.results_content = $("div.results-content");
        this.results_text = $(".result-text");
        this.scan_duration = $(".scan-duration");
    };
}

(function() {

    let covxray = new CovXray();

    // reset everything
    $(covxray.scanning_animation).css("display", "none");
    $(covxray.xray_scan_preview).css("background-url", "/static/img/xray-scan-default.png");
    $(covxray.xray_image).val('');
    $(covxray.results_content).css("display", "none");
    $(covxray.results_text).text("");
    $(covxray.scan_duration).text("");

    // event handlers
    $(covxray.scan_btn).on("click", ()=> {
        $(covxray.xray_image)[0].click();
    });

    $(covxray.xray_image).on("change", ()=> {
        const selected_image = $(covxray.xray_image)[0].files[0];

        if (selected_image.length == 0) {
            console.log("Did not select any image, so aborting");
            return;
        }

        // show the preview in the xray preview ima
        $(covxray.xray_scan_preview).css(
            "background-image"
            , `url(${URL.createObjectURL(new Blob($(covxray.xray_image)[0].files))})`
        );

        let ajax_data = new FormData();
        ajax_data.append("csrfmiddlewaretoken", $(covxray.csrf_token).val());
        ajax_data.append("xray_scan_img", selected_image);

        let start_time = new Date();

        $.ajax({
            url: "/",
            type: "POST",
            processData: false,
            contentType: false,
            data: ajax_data,
            beforeSend: function() {
                $(covxray.scan_btn).attr("disabled", "");
                $(covxray.scan_btn).text("Working please wait...");
                $(covxray.scanning_animation).css("display", "block");
                $(covxray.results_content).css("display", "none");
                $(covxray.scan_duration).text("");
            },
            success: function(response) {
                const resp = response;
                if (resp["error"] == true) {
                    alert(resp['error_msg']);
                    return;
                } 
                else  {
                    $(covxray.results_content).css("display", "block");
                    if (resp["has_covid"] == true) {
                        $(covxray.results_text).removeClass();
                        $(covxray.results_text).addClass("result-text text-danger");
                        $(covxray.results_text).text("Attention: You have COVID-19, please go to the nearest hospital as early as possible.");
                        return;
                    } 
                    else if (resp["has_viral"] == true) {
                        $(covxray.results_text).removeClass();
                        $(covxray.results_text).addClass("result-text text-info");
                        $(covxray.results_text).text("It looks like you have viral fever, as precaution please visit a doctor at the earliest.");
                        return;
                    }
                    else if (resp["is_normal"] == true) {
                        $(covxray.results_text).removeClass();
                        $(covxray.results_text).addClass("result-text text-primary");
                        $(covxray.results_text).text("Congratulations, you are absolutely alright. Hurray!");
                        return;
                    } else {
                        $(covxray.results_text).removeClass();
                        $(covxray.results_text).addClass("result-text text-danger");
                        $(covxray.results_text).text("Error: No response received from server. Contact developers.");
                        return;
                    }
                }  
            },
            complete: function() {
                $(covxray.scan_btn).removeAttr("disabled");
                $(covxray.scan_btn).text("Select X-ray scan");
                $(covxray.scanning_animation).css("display", "none");
            },
            error: function() {
                alert("There was an error, check console immediately.");
            }
        });

        let 
            end_time = new Date()
            , elasped_time = end_time - start_time
        ;
        $(covxray.scan_duration).text(`Completed scan in ${elasped_time/1000} seconds.`);
    });
}) ();