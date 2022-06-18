from libs.sitpos_predict.classifier import classifier

import argparse

parser = argparse.ArgumentParser()

if __name__ == "__main__":
    parser.add_argument("--train", help="run training script", action="store_true", default=False)
    parser.add_argument("--predict", help="run predict script", action="store_true", default=False)
    parser.add_argument("--model", help="select used model, default=RF", type=str, default="RF")
    # main(parser)
    args = parser.parse_args()
    print(args)
    cls = classifier()
    if args.train:
        cls.train(model=args.model)
    
    if args.predict:
        cls.predict_all(model=args.model)