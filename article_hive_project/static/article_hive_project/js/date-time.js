try {
  const monthNames = [
      "January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];
  const dayNames = [
  "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
  ];
  const now = new Date();
  const dayOfWeek = dayNames[now.getDay()];
  const month = monthNames[now.getMonth()];
  const dayOfMonth = now.getDate();
  const year = now.getFullYear();

  date_time = document.getElementById('date-time');
  date_time.innerHTML = `&copy; The Article Hive • ${dayOfWeek.slice(0, 3)}, ${month} ${dayOfMonth}, ${year}`;
} catch (e) {}