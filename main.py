import numpy as np
import csv

O_all = []

def calculate(_y, _m, _e, _O, _P):
  y = np.array(_y)
  y.shape = (3, 1)
  m = np.array(_m)
  m.shape = (3, 1)
  e = np.array(_e)
  e.shape = (3, 1)

  O = _O

  Z = np.linalg.norm(y) ** 2 - np.linalg.norm(m) ** 2

  h = O[:3]
  h.shape = (3, 1)
  O_all.append(np.copy(O))

  D = np.array([
    [O[3], O[6], O[7]],
    [O[6], O[4], O[8]],
    [O[7], O[8], O[5]]
  ])

  S = np.transpose(np.concatenate((y ** 2, [
    2 * y[0] * y[1],
    2 * y[0] * y[2],
    2 * y[1] * y[2]
  ])))

  J = np.transpose([
    y[0] * h[0],
    y[1] * h[1],
    y[2] * h[2],
    y[0] * h[1] + y[1] * h[0],
    y[0] * h[2] + y[2] * h[0],
    y[1] * h[2] + y[2] * h[1]
  ])

  F = [
    [2 * (1 + D[0][0]),                 0,                 0,            2 * D[0][1],            2 * D[0][2],                      0],
    [                0, 2 * (1 + D[1][1]),                 0,            2 * D[0][1],                      0,            2 * D[1][2]],
    [                0,                 0, 2 * (1 + D[2][2]),                      0,            2 * D[0][2],            2 * D[1][2]],
    [          D[0][1],           D[0][1],                 0, 2  + D[0][0] + D[1][1],                D[1][2],                D[0][2]],
    [          D[0][2],                 0,           D[0][2],                D[1][2], 2  + D[0][0] + D[2][2],                D[0][1]],
    [                0,           D[1][2],           D[1][2],                D[0][2],                D[0][1], 2  + D[1][1] + D[2][2]]
  ]

  H1 = np.matmul(2 * np.transpose(y), (np.identity(3) + D)) - 2 * np.transpose(h)
  H2 = -np.matmul(S, F) + 2 * J

  H = np.hstack((H1, H2))

  P = _P

  SIGMA = 0.2522260688
  IDyh = np.matmul((np.identity(3) + D), y) - h
  sigma2 = 4 * SIGMA ** 2 * np.matmul(np.transpose(IDyh), IDyh) + 6 * SIGMA ** 4

  K = np.matmul(
    np.matmul(P, np.transpose(H)),
    np.linalg.inv(
        np.matmul(
          np.matmul(H, P),
          np.transpose(H)
        ) + sigma2
      )
  )

  fi = np.matmul(
    np.matmul(
      -np.transpose(y),
      2 * D + D ** 2
    ),
    y
  ) + np.matmul(
    np.matmul(
      2 * np.transpose(y),
      np.identity(3) + D
    ),
    h
  ) - np.linalg.norm(h) ** 2

  Ot = np.transpose(O)
  Ot.shape = (9, 1)

  O2 = Ot + np.matmul(K, Z - fi)

  P2 = np.matmul(np.identity(9) - np.matmul(K, H), P)

  return O2, P2



time_all = []

with open('dist/iphone-calibration.csv', 'r') as fr:
  csvreader = csv.reader(fr, delimiter=';')

  m = [14.3964, 30.25, 50.837]
  e = [1, 1, 1]

  O = np.zeros(9)
  O.shape = (9, 1)

  P11 = 10 * np.identity(3)
  P12 = np.zeros((3, 6))
  P21 = np.zeros((6, 3))
  P22 = 0.001 * np.identity(6)

  P = np.vstack(( np.hstack((P11, P12)), np.hstack((P21, P22)) ))

  index = 0
  for row in csvreader:
    index += 1
    if index == 1:
      continue

    time_all.append(row[0])

    y = list(map(lambda v: float(v.replace(',', '.')), row[1:4]))

    (O, P) = calculate(y, m, e, np.transpose(O)[0], P)


  h = O[:3]
  h.shape = (3, 1)
  O_all.append(np.copy(O))

  D = np.array([
    [O[3], O[6], O[7]],
    [O[6], O[4], O[8]],
    [O[7], O[8], O[5]]
  ])
  D.shape = (3, 3)

  T = np.linalg.inv(np.identity(3) + D)

  print('h = ')
  print(h)
  print('T = ')
  print(T)
  print('T.shape = ')
  print(T.shape)



with open('dist/o.csv', 'w', newline='') as fw:
  csvwriter = csv.writer(fw, delimiter=';')

  for i in range(len(time_all)):
    csvwriter.writerow([time_all[i].replace(',', '.'), *O_all[i]])