const isValidElement = (element) => {
  return element.name && element.value;
};

// Reduce is used here because elements is technically not an array
const formToObject = (elements) =>
  [].reduce.call(
    elements,
    (data, element) => {
      if (isValidElement(element)) {
        data[element.name] = element.value;
      }
      return data;
    },
    {}
  );

async function sendItemForm(data = {}) {
  const response = await fetch("/api/itemform", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: data,
  });

  return response.json();
}

const handleFormSubmit = (event) => {
  event.preventDefault();

  const data = formToObject(form.elements);
  const dataJson = JSON.stringify(data, null, "   ");

  // const dataDisplay = document.getElementById("display_results");
  // dataDisplay.textContent = dataJson;

  const compImage = document.getElementById("comp_image");
  sendItemForm(dataJson).then((best_comp) => {
    console.log(best_comp);

    console.log("../res/" + best_comp["picture"]);
    compImage.src = "../static/" + best_comp["picture"];
    window.scrollBy(0, 500);
  });
};

const form = document.getElementById("item_form");
form.addEventListener("submit", handleFormSubmit);
