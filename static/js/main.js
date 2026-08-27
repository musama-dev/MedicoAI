// Limit how often a function can run, used for the autocomplete input.
function debounce(fn, delay) {
  let timer;
  return function () {
    const args = arguments;
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

// Escape HTML so user and bot text cannot inject markup or scripts.
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

$(document).ready(function () {
  symptoms = JSON.parse(symptoms);
  let input = $("#message-text");
  let sendBtn = $("#send");
  let startOverBtn = $("#start-over");
  let dataList = $("#symptoms-list");
  let chat = $("#conversation");

  // Handler for any input on the message input field
  input.on("input", debounce(function () {
    let insertedValue = $(this).val();
    $("#symptoms-list").empty();

    if (insertedValue.length > 1) {
      let matches = $.fn.getSuggestedSymptoms(insertedValue);
      if (matches.length === 0) {
        $(".symptoms-list-container ").slideUp();
      } else {
        for (let i = 0; i < matches.length; i++) {
          var li = document.createElement("li");
          li.textContent = matches[i];
          dataList.append(li);
        }
        $(".symptoms-list-container ").slideDown();
      }
    } else {
      $(".symptoms-list-container ").slideUp();
    }
  }, 150));

  startOverBtn.on("click", function () {
    $.fn.startOver();
  });

  sendBtn.on("click", function () {
    $.fn.handleUserMessage();
  });

  // Handler for click on one of the suggested symptoms
  dataList.on("click", "li", function () {
    input.val($(this).text());
    $(".symptoms-list-container ").slideUp();
  });
  //todo: blur on input - does not work with suggestion item clicks

  input.on("blur", function () {
    $(".symptoms-list-container ").slideUp();
  });

  input.on("keypress", function (e) {
    if (e.which == 13) {
      $.fn.handleUserMessage();
    }
  });

  // Handler function for sending a message
  $.fn.handleUserMessage = function () {
    var text = input.val();
    if (text && !$.fn.isRequestInFlight) {
      $.fn.appendUserMessage(text);
      input.val("");
      $.fn.scrollToBottom();
      $.fn.showTypingIndicator();
      $.fn.getPredictedSymptom(text);
    }
  };

  $.fn.isRequestInFlight = false;

  $.fn.showTypingIndicator = function () {
    $("#conversation").append(
      `<div class="row message-body" id="typing-indicator"><div class="col-sm-12 message-main-receiver"><div class="receiver"><div class="message-text"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div></div></div></div>`
    );
    $.fn.scrollToBottom();
  };

  $.fn.hideTypingIndicator = function () {
    $("#typing-indicator").remove();
  };

  $.fn.scrollToBottom = function () {
    chat.scrollTop(chat.prop("scrollHeight"));
  };

  $.fn.startOver = function () {
    $.fn.getPredictedSymptom("done");
    $("#conversation").empty();
    const text =
      "Welcome! I'm Medical Chatbot, but you can call me Meddy. What symptoms are you currently experiencing? When you've entered all of your symptoms, please write '<b>Done</b>'. Make sure you enter as much symptoms as possible so the prediction can be as correct as possible.";
    $("#conversation").append(
      `<div class="row message-previous"><div class="col-sm-12 previous"></div></div><div class="row message-body"><div class="col-sm-12 message-main-receiver"><div class="receiver"><div class="message-text">${text}</div></div></div></div>`
    );
    input.val("");
  };

  // Creates the newly sent message element
  $.fn.appendUserMessage = function (rawText) {
    var text = escapeHtml(rawText);
    $("#conversation").append(
      `<div class="row message-body"><div class="col-sm-12 message-main-sender"><div class="sender"><div class="message-text">${text}</div></div></div></div>`
    );
  };

  // Bot replies are trusted server text that may include <br> and <b> markup.
  $.fn.appendBotMessage = function (text) {
    $("#conversation").append(
      `<div class="row message-body"><div class="col-sm-12 message-main-receiver"><div class="receiver"><div class="message-text">${text}</div></div></div></div>`
    );
  };

  // Retreives prediction to show as bot message
  $.fn.getPredictedSymptom = function (rawText) {
    var text = rawText;
    $.fn.isRequestInFlight = true;

    $.ajax({
      url: "/symptom",
      data: JSON.stringify({ sentence: text }),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      type: "POST",
      success: function (response) {
        $.fn.hideTypingIndicator();
        if (!again) $.fn.appendBotMessage(response.response);
      },
      error: function () {
        $.fn.hideTypingIndicator();
        $.fn.appendBotMessage("Sorry, something went wrong. Please try again.");
      },
      complete: function () {
        $.fn.isRequestInFlight = false;
      },
    });
  };

  $.fn.getSuggestedSymptoms = function (val) {
    let suggestedSymptoms = [];
    $.each(symptoms, function (i, v) {
      if (v.includes(val)) {
        suggestedSymptoms.push(v);
      }
    });
    return suggestedSymptoms.slice(0, 3);
  };
});
