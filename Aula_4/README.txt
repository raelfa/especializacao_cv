Projetos da Aula 4 da Especialização em Visão Computacional da Sigmoidal

1) canny_edges_arg.py
Neste projeto foi acrescentado o input do caminho do vídeo a ser transformado via linha de comando.

2) projeto_01_greenscreen.py
Retirada de fundo verde com opencv a partir de técnicas de Keying (selecionando o range de cores com o cv2.InRange)

3) projeto_01_alternativo.py
Retirada de fundo verde com opencv com método alternativo de Keying (criando uma máscara ao comparar o fundo da imagem com uma imagem somente de fundo e aplicnado um threshold)

4) projeto_01_input_output.py
Adicionando no projeto_01_greenscreen.py o salvamento dos vídeos gerados, também foi adicionado os caminhos de entrada e saída via linha de comando.

5) projeto_01_webcam_propria.py
Retirada de fundo verde via streaming da webcam

6) carlos_greenscreen.py
Retirada do fundo do arquivo carlos_greenscreen.mov, que necessitou de ajustar a máscara manualment para pegar todo o entorno da tela verde.
