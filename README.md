# Hotel Price Monitoring Scraper

## Setup Instructions

To set up the hotel price monitoring scraper, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rang-B/pricemonitoring.git
   cd pricemonitoring
   ```

2. **Install dependencies**:
   Ensure you have Node.js installed. Then, run:
   ```bash
   npm install
   ```

3. **Configure the scraper**:
   Edit the `config.js` file to update the settings such as the hotel URLs and monitoring intervals.

4. **Run the scraper**:
   Execute the following command to start monitoring:
   ```bash
   node scraper.js
   ```

## API Documentation

The hotel price monitoring scraper provides a simple API to manage monitoring tasks:

### Endpoints

- **GET /api/prices**: Fetch the current prices for monitored hotels.
  - **Response**: A JSON object with the current prices.

- **POST /api/monitor**: Start monitoring a new hotel.
  - **Body**:
    ```json
    {
      "url": "<hotel_url>",
      "interval": <seconds>
    }
    ```
  - **Response**: Confirmation of monitoring start.

- **DELETE /api/monitor/{id}**: Stop monitoring a hotel by ID.
  - **Response**: Confirmation of monitoring stop.

## License
This project is licensed under the MIT License.