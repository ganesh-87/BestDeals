import React from "react";

const ProductCard = (props) => {
  return (
    <div class="flex flex-row justify-between bg-white my-5 rounded-md px-6 py-7 my-6">
      <div class="flex flex-col justify-between ">
        <h1 class="text-black-800 text-1xl font-playfair font-medium py-2">
          {props.title}
        </h1>
        <div class="font-lato">Price Deal : {props.price}</div>
        <div class="font-lato">Rated by people : {props.rating}</div>
      </div>
      <div>
        <button class="bg-blue-500 rounded-lg px-6 py-3 font-lato">
          <a href={props.link}>{props.source}</a>
        </button>
      </div>
    </div>
  );
};

export default ProductCard;
