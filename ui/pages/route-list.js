export default ({ routes }) => (
  <div>
    {routes &&
      routes.map((r, i) => (
        <div key={i}>
          <h2>{r.name}</h2>
          <p>{r.area.name}</p>
          <p>{r.area.parent_area && r.area.parent_area.name}</p>
        </div>
      ))}
  </div>
);
