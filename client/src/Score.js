export default function Score ({ score }) {
  return (
    <div
      style={{
        width: 'min-content',
        height: '35px'
      }}
      className='bg-dark mx-2 mb-2 p-2 text-light rounded-3'
    >
      {score.toString().substring(0,4)}
    </div>
  )
}
