$(document).ready(function() {
    console.log("jQuery is working!");

    // 사이드바 토글
    $('#toggleSidebarBtn').click(function() {
        $('#sidebar').toggleClass('collapsed');
        $('.dashboard').toggleClass('sidebar-collapsed');
    });

    // 날짜 선택기 초기화 및 초기 데이터 로드
    initializeDatePicker();
    loadInitialData();

    // Apply 버튼 이벤트 핸들러
    $('#applyDateBtn').click(function() {
        const year = $('#yearPicker').val();
        const month = $('#monthPicker').val();
        updateDashboardData(`${year}-${month}`);
    });
});

function initializeDatePicker() {
    // 설정 가능한 최소 및 최대 연도
    const minYear = 2016;
    const maxYear = 2024;
    const currentYear = new Date().getFullYear();
    const currentMonth = new Date().getMonth() + 1;

    // 연도 선택 옵션 추가
    for (let year = minYear; year <= maxYear; year++) {
        $('#yearPicker').append(`<option value="${year}">${year}</option>`);
    }

    // 월 선택 옵션 추가
    for (let month = 1; month <= 12; month++) {
        $('#monthPicker').append(`<option value="${month}">${month}</option>`);
    }

    // 현재 날짜로 설정 (현재 날짜가 범위 내에 있는 경우만)
    if (currentYear >= minYear && currentYear <= maxYear) {
        $('#yearPicker').val(currentYear);
        $('#monthPicker').val(currentMonth);
    } else {
        $('#yearPicker').val(maxYear);
        $('#monthPicker').val(12); // 범위 밖의 경우 최신 데이터로 설정
    }
}

// 초기 데이터 로드 함수
function loadInitialData() {
    const year = $('#yearPicker').val();
    const month = $('#monthPicker').val();
    updateDashboardData(`${year}-${month}`);
}

function updateDashboardData(date) {
    console.log("Updating data for: ", date);
    $.ajax({
        url: '/update-dashboard/',
        data: {
            'date': date
        },
        success: function(response) {
            updateDashboardUI(response);
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error: " + error);
        }
    });
}

function updateDashboardUI(response) {
    console.log("Response from server:", response); // 서버 응답 로그

    updateCard('#visits-card', response.visits, response.visits_change);
    updateCard('#visitors-domestic-card', response.visitors_domestic, response.visitors_domestic_change);
    updateCard('#visitors-overseas-card', response.visitors_overseas, response.visitors_overseas_change);
    updateCard('#sales-amount-card', response.sales_amount, response.sales_amount_change);

    // 차트 업데이트 함수 호출
    updateVisitsChart(response.chartDataVisits);
    updateVisitorsByProvinceChart(response.chartDataProvinces);
    updateVisitorsByCountryChart(response.chartDataCountries);
    updateSalesAmountChart(response.chartDataSales);

    // 키워드 데이터 업데이트 함수 호출
    updateKeywordsTable(response.topKeywords);
}

function updateCard(cardId, value, change) {
    const valueElement = $(`${cardId} .value`);
    const changeElement = $(`${cardId} .change`);
    const iconElement = $(`${cardId} .icon-container img`);

    // 값과 변화율 업데이트
    valueElement.text(value.toLocaleString());
    changeElement.text(formatChange(change));

    // 변화율에 따라 아이콘과 텍스트 색상 변경
    if (change && parseFloat(change) < 0) {
        changeElement.addClass('negative').removeClass('positive');
        iconElement.attr('src', iconChartMinus);
    } else {
        changeElement.addClass('positive').removeClass('negative');
        iconElement.attr('src', iconChartPlus);
    }
}

function formatChange(value) {
    if (value === null || value === "n/a") {
        return "n/a";
    }
    const changeNum = parseFloat(value);
    return `${changeNum.toFixed(2)}%`;
}

// 방문자 수 차트 업데이트
function updateVisitsChart(chartData) {
    const ctx = document.getElementById('visitsChart').getContext('2d');

    if (window.visitsChart && typeof window.visitsChart.destroy === 'function') {
        window.visitsChart.destroy();
    }

    window.visitsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels, 
            datasets: [{
                label: 'Visitors',
                data: chartData.data,
                backgroundColor: 'rgba(104, 110, 255, 0.2)', 
                borderColor: 'rgba(104, 110, 255, 1)',
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                x: {
                    ticks: {
                        color: '#FFFFFF' // X축 라벨 색상 흰색으로 설정
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#FFFFFF' // Y축 라벨 색상 흰색으로 설정
                    }
                }
            },
            plugins: {
                legend: {
                    align: 'start', // 제목을 왼쪽 정렬
                    labels: {
                        color: '#FFFFFF' // 텍스트 색상 설정
                    }
                }
            }
        }
    });
}

// 지역별 방문자 차트 업데이트
function updateVisitorsByProvinceChart(chartData) {
    const ctx = document.getElementById('visitorsByProvinceChart').getContext('2d');

    // 상위 6개 항목만 추출
    const topLabels = chartData.labels.slice(0, 6);
    const topData = chartData.data.slice(0, 6);

    if (window.visitorsByProvinceChart && typeof window.visitorsByProvinceChart.destroy === 'function') {
        window.visitorsByProvinceChart.destroy();
    }

    window.visitorsByProvinceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: topLabels,
            datasets: [{
                label: 'Domestic Visitors',
                data: topData,
                backgroundColor: 'rgb(74, 145, 247)'
            }]
        },
        options: {
            scales: {
                y: { 
                    beginAtZero: true,
                    ticks: {
                        color: '#FFFFFF' // Y축 라벨 색상 흰색으로 설정
                    }
                },
                x: { 
                    beginAtZero: true,
                    ticks: {
                        color: '#FFFFFF' // Y축 라벨 색상 흰색으로 설정
                    }
                }
            },
            plugins: {
                legend: {
                    align: 'start',
                    labels: {
                        color: '#FFFFFF'
                    }
                }
            }
        }
    });
}

// 국가별 방문자 차트 업데이트
function updateVisitorsByCountryChart(chartData) {
    const ctx = document.getElementById('visitorsByCountryChart').getContext('2d');

    // 상위 6개 항목만 추출
    const topLabels = chartData.labels.slice(0, 6);
    const topData = chartData.data.slice(0, 6);

    if (window.visitorsByCountryChart && typeof window.visitorsByCountryChart.destroy === 'function') {
        window.visitorsByCountryChart.destroy();
    }

    window.visitorsByCountryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: topLabels,
            datasets: [{
                label: 'Overseas Visitors',
                data: topData,
                backgroundColor: 'rgb(100, 198, 100)'
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#FFFFFF' // Y축 라벨 색상 흰색으로 설정
                    }
                },
                x: {
                    ticks: {
                        color: '#FFFFFF' // Y축 라벨 색상 흰색으로 설정
                    }
                }
            },
            plugins: {
                legend: {
                    align: 'start',
                    labels: {
                        color: '#FFFFFF'
                    }
                }
            }
        }
    });
}

// 매출 차트 업데이트
function updateSalesAmountChart(chartData) {
    const ctx = document.getElementById('salesAmountChart').getContext('2d');

    if (window.salesAmountChart && typeof window.salesAmountChart.destroy === 'function') {
        window.salesAmountChart.destroy();
    }

    window.salesAmountChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels, 
            datasets: [{
                label: 'Sales Amount (억)',
                data: chartData.data, 
                backgroundColor: 'rgba(255, 99, 132, 0.2)', // red 색상
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                x: {
                    ticks: {
                        color: '#FFFFFF' // Y축 라벨 색상 흰색으로 설정
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#FFFFFF' // Y축 라벨 색상 흰색으로 설정
                    }
                }
            },
            plugins: {
                legend: {
                    align: 'start',
                    labels: {
                        color: '#FFFFFF'
                    }
                }
            }
        }
    });
}

function updateKeywordsTable(keywords) {
    const tableBody = document.querySelector('.keywords table tbody');
    tableBody.innerHTML = ''; // 기존 테이블 내용을 초기화

    keywords.forEach(keyword => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${keyword.keyword}</td>
            <td>${keyword.city}</td>
            <td>${keyword.date}</td>
            <td>${keyword.count.toLocaleString()}</td>
        `;
        tableBody.appendChild(row);
    });
}