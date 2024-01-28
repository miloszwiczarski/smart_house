function goToHome() {
    window.location.href = '{{ url_for("views.home") }}';
}

function goToDevicesInfo() {
    window.location.href = '{{ url_for("views.devices_info") }}';
}

function goToDevicesControl() {
    window.location.href = '{{ url_for("views.devices_control") }}';
}

function goToDevicesReports() {
    window.location.href = '{{ url_for("views.devices_reports") }}';
}
