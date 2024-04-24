function goPage(page) {
    window.location.href = page;
}

function changeCount(event, id, delta) {
    event.preventDefault(); // 기본 동작 막기

    var goalElement = $('#' + id);
    var currentElement = $('#' + id.replace('goal', 'current'));
    
    var goalValue = parseInt(goalElement.text()) || 0;
    var currentValue = parseInt(currentElement.text()) || 0;
    
    var newGoalValue = goalValue + delta;

    if (newGoalValue < currentValue) {
        alert('목표 수량은 현재 수량보다 작을 수 없습니다.');
        return;
    }

    if (newGoalValue < 0) {
        newGoalValue = 0;
    }

    goalElement.text(newGoalValue); 
}

