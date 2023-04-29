import React from 'react';
import './css/villa-details.css';
import './css/bulma/bulma.min.css';
import '../node_modules/flatpickr/dist/flatpickr.min.css';
import flatpickr from 'flatpickr';

function VillaDetails() {
  React.useEffect(() => {
    flatpickr("#date-range-input", {
      mode: "range",
    });
  }, []);

  return (
    <section className="section">
      <div className="container">
        <h1 className="title has-text-centered is-1" style={{ fontFamily: 'cursive' }}>
          Mountain Retreat
        </h1>
        <div className="images-grid">
          <img src="mountain_view.jpg" alt="Image 1" />
          <img src="images/mountain1.jpg" alt="Image 2" />
          <img src="images/mountain2.jpg" alt="Image 3" />
          <img src="images/mountain3.jpg" alt="Image 4" />
          <img src="images/mountain4.jpg" alt="Image 5" />
          <img src="images/mountain5.jpg" alt="Image 6" />
        </div>
        <form
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            width: '100%',
          }}
        >
          <div className="field">
            <label className="label">Property Name</label>
            <div className="control">
              <input className="input" type="text" placeholder="Property Name" />
            </div>
          </div>
          <div className="field">
            <label className="label">Location</label>
            <div className="control">
              <input className="input" type="text" placeholder="Location" />
            </div>
          </div>
          <div className="field">
            <label className="label">Date Range</label>
            <div className="control">
              <input
                className="input"
                type="text"
                id="date-range-input"
                placeholder="Choose Date"
              />
            </div>
          </div>
          <div className="field">
            <label className="label">Price</label>
            <div className="control">
              <input className="input" type="text" placeholder="Price" />
            </div>
          </div>
          <div className="field">
            <label className="label">Amenities</label>
            <div className="control">
              <div className="select">
                <select>
                  <option>Swimming Pool</option>
                  <option>Sauna</option>
                  <option>Gym</option>
                  <option>Outdoor Picnic Table</option>
                  <option>Basketball Court</option>
                </select>
              </div>
            </div>
          </div>
          <div className="field is-grouped">
            <div className="control">
              <button className="button is-link">Submit</button>
            </div>
            <div className="control">
              <button className="button is-text">
                <a href="/csc309-project/P1/htmls/Properties/PropertyInfo.html">
                  Cancel
                </a>
              </button>
            </div>
          </div>
        </form>
      </div>
    </section>
  );
}

export default VillaDetails;
