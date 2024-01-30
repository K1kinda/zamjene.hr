from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    
    @app.template_filter('split')
    def split_filter(value, delimiter='|'):
        return value.split(delimiter)