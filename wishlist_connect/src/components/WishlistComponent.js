import React, { useState, useEffect } from 'react';
import axios from 'axios';

const WishlistComponent = () => {
  const [wishlist, setWishlist] = useState([]);

  useEffect(() => {
    // Fetch user's wishlist on component mount
    fetchWishlist();
  }, []);

  const fetchWishlist = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/wishlist/');
      setWishlist(response.data);
    } catch (error) {
      console.error('Error fetching wishlist:', error);
    }
  };

  return (
    <div>
      <h2>Your Wishlist</h2>
      <ul>
        {wishlist.map((gift) => (
          <li key={gift.id}>{gift.title} - {gift.description}</li>
        ))}
      </ul>
    </div>
  );
};

export default WishlistComponent;
