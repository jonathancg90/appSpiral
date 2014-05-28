describe("Scripts", function() {
    it("comapre resul math", function() {
        var a = 10,
            b = 20,
            result  = a + b;
        expect(calculator.sum(a,b)).toEqual(result);
    });

    it('compare status', function(){
        var status = true;

        expect(status).toBe(true);
    });

    it('compare string regular expresion', function(){
        var texto = 'Hello World Peru';

        expect(texto).toMatch(/World/);
    });

    it('compare matches defined', function(){
        var libro = {
            "autor": "Jonathan",
            "nombre": "la historia sin fin"
        };

        expect(libro.autor).toBeDefined();
        expect(libro.editorial).toBeUndefined();

    });
});