<script>
    import { chart } from "svelte-apexcharts";
    export let chartType = "bar";
    let options = {
        chart: {
            type: chartType,
            height: '300px',
            toolbar: {
                show: false
            },
        },
        series: [
            {
                name: "Försäljning (tkr)",
                data: [30, 40, 35, 50, 49, 60, 70, 91, 125]
            }
        ],
        xaxis: {
            categories: [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]
        },
        yaxis: {
            title: {
                text: "Försäljning (tkr)"
            }
        }
    };
</script>

<div use:chart={options} />

<style>

</style>