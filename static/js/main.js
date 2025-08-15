'use strict';

/**
 * タスク完了・未完了トグルのイベントを設定
 */
document.querySelectorAll('.toggle-checkbox').forEach((checkbox) => {
  checkbox.addEventListener('change', handleToggleChange);
});

/**
 * タスクの削除ボタンのイベントを設定
 */
document.querySelectorAll('.delete-task').forEach((button) => {
  button.addEventListener('click', handleDeleteClick);
});

document.querySelector('.task-input').addEventListener('input', () => {
  input.classList.remove('error');
});
/**
 * タスク追加ボタンのイベントを設定
 */
document.querySelector('.add-task').addEventListener('click', handleAddClick);

/**
 * タスク追加の処理
 */
async function handleAddClick(event) {
  event.preventDefault();
  const input = document.querySelector('.task-input');
  const content = input.value.trim();
  if (content !== '') {
    const response = await fetch(`/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ value: content }),
    });
    const data = await response.json();
    if (!data.success) {
      alert('状態の更新に失敗しました');
      return;
    }
    const li = document.createElement('li');
    li.textContent = content;
    moveTaskBetweenLists(li, false, data.id);
    input.value = '';
  } else {
    input.value = '';
    input.focus();
    input.classList.add('error');
    input.addEventListener('input', () => {
      input.classList.remove('error');
    });
  }
}

/**
 * タスクを完了・未完了リストへ移動し、HTMLを更新
 */
function moveTaskBetweenLists(li, completed, taskId) {
  const taskText = li.textContent;

  li.classList.add('fade-out');

  setTimeout(() => {
    // チェックボックス・ラベル・削除ボタンを再生成
    li.innerHTML = `
      <input type="checkbox" class="toggle-checkbox" data-id="${taskId}" id="check-${taskId}" ${
      completed ? 'checked' : ''
    }>
      <label for="check-${taskId}" data-content="${taskText}" id="content-${taskId}">${taskText}</label>
      <button class="round_btn delete-task" data-id="${taskId}"></button>
    `;

    // 再度イベントリスナーを定義
    const newCheckbox = li.querySelector('.toggle-checkbox');
    newCheckbox.addEventListener('change', handleToggleChange);

    const newDeleteButton = li.querySelector('.delete-task');
    newDeleteButton.addEventListener('click', handleDeleteClick);

    // リスト移動
    const targetListId = completed ? 'complete-list' : 'incomplete-list';
    document.getElementById(targetListId).appendChild(li);

    li.classList.remove('fade-out');
    li.classList.add('fade-in');
    setTimeout(() => li.classList.remove('fade-in'), 500);
  }, 400);
}

/**
 * タスク完了・未完了トグル処理
 */
async function handleToggleChange(event) {
  const checkbox = event.target;
  const taskId = checkbox.dataset.id;
  try {
    const response = await fetch(`/toggle/${taskId}`, {
      method: 'POST',
    });
    const data = await response.json();
    if (!data.success) {
      alert('状態の更新に失敗しました');
      return;
    }

    // ご褒美ボタン表示
    if (data.completed) {
      const rewardButton = document.getElementById('reward-button-area');
      if (rewardButton) rewardButton.classList.add('show');
    }

    // リスト更新
    const li = checkbox.closest('li');
    moveTaskBetweenLists(li, data.completed, taskId);
  } catch (error) {
    console.error(error);
    alert('通信エラーが発生しました');
  }
}

/**
 * タスク削除処理
 */
async function handleDeleteClick(event) {
  event.preventDefault();
  const button = event.target;
  const taskId = button.dataset.id;
  try {
    const response = await fetch(`/delete/${taskId}`, {
      method: 'DELETE',
    });
    const data = await response.json();
    if (!data.success) {
      alert('状態の更新に失敗しました');
      return;
    }
    const taskElement = button.closest('li');
    taskElement.classList.add('fade-out');
    setTimeout(() => taskElement.remove(), 300);
  } catch (error) {
    console.error(error);
    alert('通信エラーが発生しました');
  }
}

/**
 * 未完了リストの並び替え保存（Sortable.js）
 */
const incompleteList = document.getElementById('incomplete-list');

new Sortable(incompleteList, {
  animation: 150,
  onEnd: function () {
    const orderedIds = Array.from(incompleteList.children).map(
      (li) => li.querySelector('.toggle-checkbox').dataset.id
    );

    fetch('/reorder', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ordered_ids: orderedIds }),
    });
  },
});
