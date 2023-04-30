import React, { useState, useEffect } from "react";
import axios from "axios";
import "./css/HotelAvailability.css";
import { useLocation } from "react-router-dom";

export default function Hotel_Availability() {
  const [availability, setAvailability] = useState([]);
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem("token");
  const location = useLocation();
  const hotel_id = location.state?location.state.hotel_id:-1;
  console.log("Hotel ID:", hotel_id);
  useEffect(() => {
    axios
      .get("http://localhost:8000/hotels/search/availability/", {
        headers: { Authorization: "Bearer " + token }, 
        params: {hotel: hotel_id},
      })
      .then((response) => {
        console.log("API Response:", response.data);
        setAvailability(response.data.results);
        setLoading(false);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);
  
  const handleUpdateAvailability = (event, id) => {
    event.preventDefault();
    const form = event.target.closest("form");
    const start_date = form.querySelector(".start_date_input").value;
    const end_date = form.querySelector(".end_date_input").value;
    const price = form.querySelector(".price-input").value;

    axios
      .put(
        //update/<int:pk>/availability/
        `http://localhost:8000/hotels/update/${id}/availability/`,
        {
          start_date,
          end_date,
          price,
        },
        {
          headers: { Authorization: "Bearer " + token },
        }
      )
      .then((response) => {
        console.log(response);
        const updatedAvailability = availability.map((value, index) => {
          if (value.id === id) {
            return { ...value, start_date, end_date, price };
          }
          return value;
        });

        setAvailability(updatedAvailability);
      })
      .catch((error) => {
        console.log(error);
      });
  };
  const handleReturn = () => {return(loading ? (
    <p>Loading...</p>
  ) : (
    <ul>
      {availability.map((value, index) => (
        <li key={value.id}>
          <form onSubmit={(event) => handleUpdateAvailability(event, value.id)}>
            <label>
              Start Date:
              <input
                type="date"
                className="start_date_input"
                defaultValue={value.start_date}
              />
            </label>
            <label>
              End Date:
              <input
                type="date"
                className="end_date_input"
                defaultValue={value.end_date}
              />
            </label>
            <label>
              Price:
              <input
                type="number"
                className="price-input"
                defaultValue={value.price}
              />
            </label>
            <button type="submit">Update</button>
          </form>
        </li>
      ))}
    </ul>
  ))}

  return (
    <div className="hotel-availability">
      <h2>Hotel Availability</h2>
    { handleReturn() } 
    </div>
  );
}
